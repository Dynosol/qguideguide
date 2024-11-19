# courses/views.py
from django.shortcuts import render
from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer

def landing_page(request):
    courses = Course.objects.all()
    return render(request, 'base.html', {'courses': courses})

def about(request):
    return render(request, 'about.html')

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('title')
    serializer_class = CourseSerializer
