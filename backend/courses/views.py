from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_datatables import filters as dt_filters
from .models import Course
from .serializers import CourseSerializer
from rest_framework.pagination import LimitOffsetPagination
from django.utils.http import http_date, quote_etag
from core.cache_utils import cache, get_cached_data
from django.db import connection
import hashlib
import json

REQUEST_LIMIT = None

class CoursePagination(LimitOffsetPagination):
    default_limit = REQUEST_LIMIT

def generate_etag(data):
    """Generate an ETag from the data"""
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_queryset(self):
        """Get queryset with proper connection handling"""
        connection.close()  # Close any stale connections
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        try:
            # Try to get from cache first
            data = get_cached_data('courses_data')
            if data:
                return Response(data)

            # If not in cache, get from database with proper connection handling
            connection.ensure_connection()  # Ensure we have a fresh connection
            queryset = self.get_queryset().order_by('title')
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = self.get_paginated_response(serializer.data).data
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
            
            # Cache the result
            cache.set('courses_data', data, timeout=86400)
            return Response(data)
        finally:
            connection.close()  # Always close the connection when done
