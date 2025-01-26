from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses.views import CourseViewSet
from professors.views import ProfessorViewSet, DepartmentViewSet
from django.views.generic import TemplateView
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django_redis import get_redis_connection  # Import get_redis_connection
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

api_router = DefaultRouter()
api_router.register(r'courses', CourseViewSet, basename='course')
api_router.register(r'professors', ProfessorViewSet, basename='professor')
api_router.register(r'departments', DepartmentViewSet, basename='department')

@require_GET
def health_check(request):
    status = {
        "status": "OK",
        "service": "QGuideGuide",
        "timestamp": timezone.now().isoformat(),
        "checks": {}
    }
    
    # Database check
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status["checks"]["database"] = {"status": "OK"}
    except Exception as e:
        status["checks"]["database"] = {
            "status": "ERROR",
            "message": str(e)
        }
        status["status"] = "ERROR"
    
    # Cache check
    try:
        from django.core.cache import cache
        cache.set('health_check', 'ok', 1)
        if cache.get('health_check') == 'ok':
            status["checks"]["cache"] = {"status": "OK"}
        else:
            raise Exception("Cache set/get failed")
    except Exception as e:
        status["checks"]["cache"] = {
            "status": "ERROR",
            "message": str(e)
        }
        status["status"] = "ERROR"
    
    # Redis check
    try:
        redis_conn = get_redis_connection("default")
        redis_conn.ping()
        status["checks"]["redis"] = {"status": "OK"}
    except Exception as e:
        status["checks"]["redis"] = {
            "status": "ERROR",
            "message": str(e)
        }
        status["status"] = "ERROR"
    
    return JsonResponse(status, status=200 if status["status"] == "OK" else 503)

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Health check endpoint
    path('healthz/', health_check, name='health_check'),

    # API endpoints
    path('api/', include(api_router.urls)),

    # Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]