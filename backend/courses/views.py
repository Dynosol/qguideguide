from django.shortcuts import render
from rest_framework import viewsets, pagination
from .models import Course
from rest_framework.pagination import LimitOffsetPagination
from .serializers import CourseSerializer
from django.utils.http import http_date
from django.db.models import Max
from datetime import datetime
from rest_framework.response import Response
from core.cache_utils import get_cached_data

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
        # Get data from cache
        data = get_cached_data('courses_data')
        
        # Handle pagination
        page = self.paginate_queryset(data)
        if page is not None:
            return self.get_paginated_response(page)
        
        return Response(data)

    def head(self, request, *args, **kwargs):
        latest_update = Course.objects.aggregate(Max('modified_at'))['modified_at__max']
        response = Response(None, status=200)
        if latest_update:
            response['Last-Modified'] = http_date(latest_update.timestamp())
        return response
