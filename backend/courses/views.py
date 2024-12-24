from django.shortcuts import render
from rest_framework import viewsets, pagination
from .models import Course
from rest_framework.pagination import LimitOffsetPagination
from .serializers import CourseSerializer

REQUEST_LIMIT = None

# def courses_list(request):
#     courses = Course.objects.all()
#     return render(request, 'courses.html', {'courses': courses})

class CoursePagination(LimitOffsetPagination):
    default_limit = REQUEST_LIMIT  # Number of records per page

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('title')
    serializer_class = CourseSerializer
    pagination_class = CoursePagination
