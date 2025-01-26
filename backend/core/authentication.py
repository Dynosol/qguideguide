from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings

class AnonymousJWTAuthentication(BaseAuthentication):
    """
    Custom authentication class that creates JWT tokens for anonymous users
    and validates existing tokens.
    """
    def authenticate(self, request):
        # Check for existing JWT token
        header = request.headers.get('Authorization')
        
        if not header:
            # Create new anonymous user and token if no token exists
            user = AnonymousUser()
            refresh = RefreshToken()
            
            # Add custom claims
            refresh['anonymous'] = True
            refresh['session_id'] = request.session.session_key or 'new_session'
            
            # Set token in response headers
            request.anonymous_token = str(refresh.access_token)
            return (user, refresh.access_token)
            
        try:
            # Validate existing token
            token = header.split(' ')[1]
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            
            if payload.get('anonymous', False):
                return (AnonymousUser(), token)
            
        except (jwt.InvalidTokenError, IndexError):
            raise AuthenticationFailed('Invalid token')
        
        return None

    def authenticate_header(self, request):
        return 'Bearer'
