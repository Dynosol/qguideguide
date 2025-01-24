from django.http import JsonResponse
from django.conf import settings

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip API key check for OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            response = self.get_response(request)
            # Ensure CORS headers are set for preflight
            response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
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
            if not api_key or api_key != settings.API_KEY:
                return JsonResponse({'error': 'Invalid API key'}, status=403)
        
        response = self.get_response(request)
        
        # Always ensure CORS headers are present
        origin = request.headers.get('Origin')
        if origin:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
        
        return response