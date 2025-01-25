from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
import time
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.urls import resolve

# Set up loggers
security_logger = logging.getLogger('security')
api_logger = logging.getLogger('api')

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

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

        # Skip JWT check for OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            response = self.get_response(request)
            origin = request.headers.get('Origin')
            
            # Always set CORS headers for OPTIONS requests, regardless of origin
            # This ensures cached responses also have proper CORS headers
            if origin:
                allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
                if settings.DEBUG or origin in allowed_origins:
                    response['Access-Control-Allow-Origin'] = origin
                    response['Access-Control-Allow-Credentials'] = 'true'
                    response['Access-Control-Allow-Headers'] = 'Authorization, Content-Type, Accept, X-API-Key'
                    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, HEAD, OPTIONS'
                    response['Access-Control-Max-Age'] = '3600'  # Cache preflight for 1 hour
                    response['Access-Control-Expose-Headers'] = 'last-modified'
                    
                    # Ensure the response is not cached by Redis
                    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                    response['Pragma'] = 'no-cache'
                    response['Expires'] = '0'
            
            return response

        # For non-OPTIONS requests, ensure CORS headers are set
        response = self.get_response(request)
        origin = request.headers.get('Origin')
        if origin and (settings.DEBUG or origin in getattr(settings, 'CORS_ALLOWED_ORIGINS', [])):
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Expose-Headers'] = 'last-modified'

        # Skip JWT check for development if DEBUG is True
        if settings.DEBUG:
            return response

        # Skip JWT check for non-API routes and token endpoints
        if not request.path.startswith('/api/') or request.path in ['/api/token/', '/api/token/refresh/']:
            return response

        try:
            # Get the Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return JsonResponse(
                    {'error': 'Authorization header is missing'}, 
                    status=401
                )

            # Validate the JWT token
            validated_token = self.jwt_auth.get_validated_token(
                self.jwt_auth.get_raw_token(auth_header)
            )
            
            # Add the validated token to the request for use in views
            request.validated_token = validated_token
            
            return response

        except (InvalidToken, TokenError) as e:
            return JsonResponse(
                {'error': str(e)}, 
                status=401
            )

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