from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseTooManyRequests
import time
import logging

# Set up loggers
security_logger = logging.getLogger('security')
api_logger = logging.getLogger('api')

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip API key check for OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            response = self.get_response(request)
            origin = request.headers.get('Origin')
            if origin and (settings.DEBUG or origin in getattr(settings, 'CORS_ALLOWED_ORIGINS', [])):
                response['Access-Control-Allow-Origin'] = origin
                response['Access-Control-Allow-Credentials'] = 'true'
                response['Access-Control-Allow-Headers'] = 'x-api-key, content-type'
                response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
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
                    'user': request.user.username if request.user.is_authenticated else 'anonymous'
                }
            )
            
            if not api_key or api_key != settings.API_KEY:
                # Log security event
                security_logger.warning(
                    'Invalid API key attempt',
                    extra={
                        'ip': client_ip,
                        'path': request.path,
                        'user': request.user.username if request.user.is_authenticated else 'anonymous'
                    }
                )
                return JsonResponse({'error': 'Invalid API key'}, status=403)
        
        response = self.get_response(request)
        
        # Always ensure CORS headers are present
        origin = request.headers.get('Origin')
        if origin and (settings.DEBUG or origin in getattr(settings, 'CORS_ALLOWED_ORIGINS', [])):
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
        
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
        if request.method != 'OPTIONS' and request.path.startswith('/api/'):
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
                        'user': request.user.username if request.user.is_authenticated else 'anonymous',
                        'request_count': len(requests)
                    }
                )
                return HttpResponseTooManyRequests("Rate limit exceeded. Please try again later.")
            
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
                        'user': request.user.username if request.user.is_authenticated else 'anonymous',
                        'request_count': len(requests)
                    }
                )
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')