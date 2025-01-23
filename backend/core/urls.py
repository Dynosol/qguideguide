"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from rest_framework.routers import DefaultRouter
from courses.views import CourseViewSet
from professors.views import ProfessorViewSet, DepartmentViewSet

# Create custom router without API root
class CustomRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        # Disable API root view
        return None

# Create API router
api_router = CustomRouter()
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
    
    # Static files check
    try:
        from django.contrib.staticfiles.finders import get_finder
        finder = get_finder('django.contrib.staticfiles.finders.FileSystemFinder')
        if finder.find('favicon.ico'):
            status["checks"]["static_files"] = {"status": "OK"}
        else:
            raise Exception("Static files not found")
    except Exception as e:
        status["checks"]["static_files"] = {
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

    # Main application routes - these are public
    path('', CourseViewSet.as_view({'get': 'list'}), name='home'),
    path('professors/', ProfessorViewSet.as_view({'get': 'list'}), name='professors'),
    path('departments/', DepartmentViewSet.as_view({'get': 'list'}), name='departments'),
    
    # API endpoints - hidden from browsing
    path('api/v1/', include(api_router.urls)),
    
    # Static pages
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
]
