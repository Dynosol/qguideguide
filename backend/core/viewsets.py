from rest_framework import viewsets, permissions
from core.throttling import APIEndpointRateThrottle

class ThrottledViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet that includes rate limiting and JWT authentication
    """
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [APIEndpointRateThrottle]
