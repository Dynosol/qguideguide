from django.http import JsonResponse
from django.conf import settings

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip API key check for OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            return self.get_response(request)

        # Skip API key check for development
        if settings.DEBUG:
            return self.get_response(request)

        # Only check API routes
        if request.path.startswith('/api/'):
            api_key = request.headers.get('X-API-Key')
            if not api_key or api_key != settings.API_KEY:
                return JsonResponse({'error': 'Invalid API key'}, status=403)
        
        response = self.get_response(request)
        
        # Ensure CORS headers are preserved
        if 'Access-Control-Allow-Origin' not in response:
            response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        if 'Access-Control-Allow-Credentials' not in response:
            response['Access-Control-Allow-Credentials'] = 'true'
        
        return response