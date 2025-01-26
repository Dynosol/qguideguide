from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
import time
import logging
from django.urls import resolve
import secrets

# Set up loggers
security_logger = logging.getLogger('security')
api_logger = logging.getLogger('api')

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 1000  # requests per minute
        self.window = 60  # seconds

    def __call__(self, request):
        # Log all headers for debugging
        api_logger.info(
            'Request Headers',
            extra={
                'headers': dict(request.headers),
                'method': request.method,
                'path': request.path
            }
        )

        if request.method not in ['OPTIONS', 'HEAD'] and request.path.startswith('/api/'):
            ip = self.get_client_ip(request)
            key = f'rate_limit:{ip}'
            
            # Get the current request count
            requests = cache.get(key, [])
            now = time.time()
            
            # Filter out requests older than our window
            requests = [req for req in requests if now - req < self.window]
            
            if len(requests) >= self.rate_limit:
                # Log rate limit exceeded
                security_logger.warning(
                    'Rate limit exceeded',
                    extra={
                        'ip': ip,
                        'path': request.path,
                        'user': 'anonymous',  # Simplified as we don't need user info for rate limit logging
                        'request_count': len(requests)
                    }
                )
                return HttpResponse("Rate limit exceeded. Please try again later.", status=429)
            
            # Add the current request and update the cache
            requests.append(now)
            cache.set(key, requests, self.window)
            
            # Log if approaching rate limit
            if len(requests) > self.rate_limit * 0.8:  # 80% of limit
                security_logger.warning(
                    'Approaching rate limit',
                    extra={
                        'ip': ip,
                        'path': request.path,
                        'user': 'anonymous',  # Simplified as we don't need user info for rate limit logging
                        'request_count': len(requests)
                    }
                )
        
        response = self.get_response(request)
        
        # Add CORS headers for successful responses
        if request.path.startswith('/api/'):
            origin = request.headers.get('Origin')
            if origin and (settings.DEBUG or origin in getattr(settings, 'CORS_ALLOWED_ORIGINS', [])):
                response['Access-Control-Allow-Origin'] = origin
                response['Access-Control-Allow-Credentials'] = 'true'
                response['Access-Control-Expose-Headers'] = 'last-modified'
                
                # Add cache control headers - allow caching but require revalidation
                response['Cache-Control'] = 'no-cache, must-revalidate'
                response['Pragma'] = 'no-cache'
                
                # Handle HEAD requests same as GET
                if request.method in ['HEAD', 'GET']:
                    response['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
                    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, HEAD, OPTIONS'
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class SessionTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow OPTIONS requests to pass through without token check
        if request.method == 'OPTIONS':
            return self.get_response(request)

        if request.path.startswith('/api/'):
            # Skip token validation for the first request
            is_first_request = not request.headers.get('X-Session-Token')
            session_token = request.session.get('api_token')

            if is_first_request:
                # Generate new token if none exists
                if not session_token:
                    session_token = secrets.token_urlsafe(32)
                    request.session['api_token'] = session_token
                    request.session.set_expiry(86400)  # 24 hours
            else:
                # Validate token for subsequent requests
                request_token = request.headers.get('X-Session-Token')
                if not request_token or request_token != session_token:
                    return JsonResponse({'error': 'Invalid session token'}, status=401)

        response = self.get_response(request)
        
        # Add token to response headers for all API requests
        if request.path.startswith('/api/'):
            response['X-Session-Token'] = request.session['api_token']
            # Add CORS headers specifically for the token
            response['Access-Control-Expose-Headers'] = 'X-Session-Token, ' + response.get('Access-Control-Expose-Headers', '')
        
        return response