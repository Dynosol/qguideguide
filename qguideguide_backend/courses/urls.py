# courses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet, basename='course')

urlpatterns = [
    path('api/', include(router.urls)),  # Register the API URLs
    path('', views.landing_page, name='landing_page'),  # Root page for courses
    path('about/', views.about, name='about'),  # About page for courses
]
