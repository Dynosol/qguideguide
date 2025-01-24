from rest_framework import viewsets
from core.throttling import APIEndpointRateThrottle

class ThrottledViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet that includes rate limiting
    """
    throttle_classes = [APIEndpointRateThrottle]
