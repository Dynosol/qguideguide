from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.cache import cache
import time
import logging

# Set up loggers
security_logger = logging.getLogger('security')
api_logger = logging.getLogger('api')

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

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

        # Skip API key check for OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            response = self.get_response(request)
            origin = request.headers.get('Origin')
            if origin and (settings.DEBUG or origin in getattr(settings, 'CORS_ALLOWED_ORIGINS', [])):
                response['Access-Control-Allow-Origin'] = origin
                response['Access-Control-Allow-Credentials'] = 'true'
                response['Access-Control-Allow-Headers'] = 'x-api-key, content-type'
                response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, HEAD, OPTIONS'
                response['Access-Control-Expose-Headers'] = 'last-modified'
            return response

        # Skip API key check for development
        if settings.DEBUG:
            return self.get_response(request)

        # Only check API routes
        if request.path.startswith('/api/'):
            api_key = request.headers.get('X-API-Key')
            client_ip = self.get_client_ip(request)
            
            # Log API access
            api_logger.info(
                'API Request',
                extra={
                    'ip': client_ip,
                    'path': request.path,
                    'method': request.method,
                    'api_key_present': bool(api_key),
                    'api_key_matches': api_key == settings.API_KEY
                }
            )
            
            if not api_key or api_key != settings.API_KEY:
                # Log security event
                security_logger.warning(
                    'Invalid API key attempt',
                    extra={
                        'ip': client_ip,
                        'path': request.path,
                        'method': request.method,
                        'provided_key': api_key,
                        'expected_key': settings.API_KEY
                    }
                )
                return JsonResponse({'error': 'Invalid API key'}, status=403)

        response = self.get_response(request)
        
        # Add CORS headers for successful responses
        if request.path.startswith('/api/'):
            origin = request.headers.get('Origin')
            if origin and (settings.DEBUG or origin in getattr(settings, 'CORS_ALLOWED_ORIGINS', [])):
                response['Access-Control-Allow-Origin'] = origin
                response['Access-Control-Allow-Credentials'] = 'true'
                response['Access-Control-Expose-Headers'] = 'last-modified'
                # Add cache control headers
                response['Cache-Control'] = 'no-cache'
                if request.method == 'HEAD':
                    response['Access-Control-Allow-Headers'] = 'x-api-key, content-type'
                    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, HEAD, OPTIONS'
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 100  # requests per minute
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
                # Add cache control headers
                response['Cache-Control'] = 'no-cache'
                if request.method == 'HEAD':
                    response['Access-Control-Allow-Headers'] = 'x-api-key, content-type'
                    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, HEAD, OPTIONS'
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')