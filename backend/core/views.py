from django.urls import path
from core import views
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache
from django.db import connection

def landing_page(request):
    return render(request, 'base.html')  # Ensure 'base.html' exists and is correctly referenced

@api_view(['GET', 'HEAD'])
def health_check(request):
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        return Response({"status": "error", "detail": "Database unavailable"}, status=503)

    # Check Redis connection
    try:
        cache.get('health_check')
    except Exception:
        return Response({"status": "error", "detail": "Cache unavailable"}, status=503)

    return Response({"status": "healthy"}, status=200)