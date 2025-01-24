from rest_framework import throttling

class TokenRateThrottle(throttling.AnonRateThrottle):
    rate = '1/minute'
    scope = 'token_gen'

    def get_cache_key(self, request, view):
        # Use IP address for rate limiting token generation
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

class APIEndpointRateThrottle(throttling.UserRateThrottle):
    rate = '50/hour'
    scope = 'api_endpoints'

    def get_cache_key(self, request, view):
        # For authenticated users, use their user ID
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            # For unauthenticated users, use their IP
            ident = self.get_ident(request)
            
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
