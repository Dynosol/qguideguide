from django.shortcuts import render
from rest_framework import viewsets, pagination
from .models import Course
from rest_framework.pagination import LimitOffsetPagination
from .serializers import CourseSerializer
from django.utils.http import http_date
from django.db.models import Max
from datetime import datetime
from rest_framework.response import Response

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

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        latest_update = Course.objects.aggregate(Max('modified_at'))['modified_at__max']
        if latest_update:
            response['Last-Modified'] = http_date(latest_update.timestamp())
        return response

    def head(self, request, *args, **kwargs):
        latest_update = Course.objects.aggregate(Max('modified_at'))['modified_at__max']
        response = Response(None, status=200)
        if latest_update:
            response['Last-Modified'] = http_date(latest_update.timestamp())
        return response
