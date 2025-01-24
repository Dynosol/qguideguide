from django.http import JsonResponse
from django.conf import settings

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip API key check for development
        if settings.DEBUG:
            return self.get_response(request)

        # Only check API routes
        if request.path.startswith('/api/'):
            api_key = request.headers.get('X-API-Key')
            if not api_key or api_key != settings.API_KEY:
                return JsonResponse({'error': 'Invalid API key'}, status=403)
        
        return self.get_response(request)
