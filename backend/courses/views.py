from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_datatables import filters as dt_filters
from .models import Course
from .serializers import CourseSerializer
from rest_framework.pagination import PageNumberPagination
from django.utils.http import http_date, quote_etag
from core.cache_utils import cache
import hashlib
import json
import zlib

class CoursesPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all().order_by('title')
    serializer_class = CourseSerializer
    pagination_class = CoursesPagination

    def list(self, request, *args, **kwargs):
        try:
            # Get page number from request
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', 100)
            
            # Generate cache key based on pagination parameters
            cache_key = f'courses_page_{page}_{page_size}'
            
            # Try to get data from cache
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(json.loads(zlib.decompress(cached_data).decode('utf-8')))

            # If not in cache, get from database
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                result = self.get_paginated_response(serializer.data)
                
                # Cache the paginated response
                compressed_data = zlib.compress(json.dumps(result.data).encode('utf-8'))
                cache.set(cache_key, compressed_data, timeout=86400)  # 24 hours
                
                return result

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            print(f"Error in CourseViewSet: {str(e)}")
            return Response({"error": "An error occurred"}, status=500)
