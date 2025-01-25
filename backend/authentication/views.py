from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.contrib.auth.models import User
from core.throttling import TokenRateThrottle
import uuid

# Create your views here.

class GetAPIToken(APIView):
    throttle_classes = [TokenRateThrottle]
    
    def post(self, request):
        # Check if the request has the API key
        api_key = request.headers.get('X-API-Key')
        
        if api_key != settings.API_KEY:
            return Response(
                {'error': 'Invalid API key'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Create or get a system user for token generation
        username = f'system_user_{uuid.uuid4().hex[:8]}'
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'is_active': True}
        )

        # Generate token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })

class CustomTokenRefreshView(TokenRefreshView):
    throttle_classes = [TokenRateThrottle]

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except User.DoesNotExist:
            return Response(
                {'error': 'Token is invalid or expired. Please obtain a new token.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
