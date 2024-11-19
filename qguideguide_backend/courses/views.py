from django.shortcuts import render
from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer

def courses_list(request):
    courses = Course.objects.all()
    print(courses)
    return render(request, 'courses.html', {'courses': courses})

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('title')
    serializer_class = CourseSerializer
