from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_datatables import filters as dt_filters
from .models import Course
from .serializers import CourseSerializer
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
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

class CoursePageNumberPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all().order_by('title')
    serializer_class = CourseSerializer
    pagination_class = None  # Disable pagination for full dataset caching

    def get_queryset(self):
        """Get queryset with proper connection handling"""
        connection.close()  # Close any stale connections
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        try:
            data = get_cached_data('courses_data')
            return Response(data)
        except Exception as e:
            connection.ensure_connection()
            try:
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            finally:
                connection.close()
