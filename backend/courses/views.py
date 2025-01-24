from django.db.models import Q, Max
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework_datatables import filters as dt_filters
from .models import Course
from .serializers import CourseSerializer, CourseListSerializer
from rest_framework.pagination import LimitOffsetPagination
from django.utils.http import http_date
from datetime import datetime
from core.cache_utils import get_cached_data, cache
from core.viewsets import ThrottledViewSet
import logging
import time

REQUEST_LIMIT = None

# def courses_list(request):
#     courses = Course.objects.all()
#     return render(request, 'courses.html', {'courses': courses})

class CoursePagination(LimitOffsetPagination):
    default_limit = REQUEST_LIMIT

logger = logging.getLogger(__name__)

class CourseViewSet(ThrottledViewSet):
    queryset = Course.objects.all().order_by('title')
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_serializer_class(self):
        """Return different serializers for list and detail"""
        if self.action == 'list':
            return CourseListSerializer
        return CourseSerializer

    def list(self, request, *args, **kwargs):
        start_time = time.time()

        # Start timing database query
        db_start_time = time.time()
        try:
            # Get data from cache
            data = get_cached_data('courses_list_data')  
            if data is None:
                # If cache completely fails, fall back to database
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
                cache.set('courses_list_data', data, 60 * 60 * 24)  
            
            # Handle pagination
            page = self.paginate_queryset(data)
            if page is not None:
                response = self.get_paginated_response(page)
            else:
                response = Response(data)
            
            # Calculate total duration
            total_duration = (time.time() - start_time) * 1000  

            # Set Server-Timing header
            response['Server-Timing'] = f"db;dur={(time.time() - db_start_time) * 1000:.2f}, total;dur={total_duration:.2f}"

            return response
        except Exception as e:
            logger.error(f"Error in CourseViewSet.list: {str(e)}")
            return Response(
                {"error": "An error occurred while fetching courses"},
                status=500
            )

    def head(self, request, *args, **kwargs):
        try:
            latest_update = Course.objects.aggregate(Max('modified_at'))['modified_at__max']
            if latest_update:
                response = Response()
                response['Last-Modified'] = http_date(datetime.timestamp(latest_update))
                return response
            return Response()
        except Exception as e:
            logger.error(f"Error in CourseViewSet.head: {str(e)}")
            return Response(status=500)
