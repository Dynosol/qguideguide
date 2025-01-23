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
from . import views 
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def health_check(request):
    # Basic check (server is running)
    status = {
        "status": "OK",
        "service": "Django Application",
        "version": "1.0.0"
    }
    
    # Optional: Add database check
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status["database"] = "OK"
    except Exception as e:
        status["database"] = "ERROR"
    
    return JsonResponse(status, status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.landing_page, name='landing_page'),
    # path('', include('courses.urls')),
    # path('courses', include('courses.urls')),
    # path('about/', include('about.urls')),
    # path('contact/', include('contact.urls')),
    # path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    # post react-ification
    path('api/courses/', include('courses.urls')),
    path('api/professors/', include('professors.urls')),
    
    path('healthz/', health_check, name="healthcheck")
]
