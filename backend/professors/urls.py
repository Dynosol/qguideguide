from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'professors', views.ProfessorViewSet, basename='professor')
router.register(r'departments', views.DepartmentViewSet, basename='department')

urlpatterns = [
    path('', include(router.urls)),
]