from rest_framework import viewsets, permissions
from core.throttling import APIEndpointRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

class ThrottledViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet that includes rate limiting and JWT authentication
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [APIEndpointRateThrottle]
