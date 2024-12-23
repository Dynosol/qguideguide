from django.shortcuts import render
from rest_framework import viewsets, pagination
from .models import Course
from .serializers import CourseSerializer

def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

class NoPagination(pagination.LimitOffsetPagination):
    default_limit = 10  # No limit to the number of records returned

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('title')
    serializer_class = CourseSerializer
    pagination_class = NoPagination
