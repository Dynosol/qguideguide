from django.db.models import Q, Max
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_datatables import filters as dt_filters
from .models import Course
from .serializers import CourseSerializer
from rest_framework.pagination import LimitOffsetPagination
from django.utils.http import http_date, quote_etag
from datetime import datetime
from core.cache_utils import get_cached_data, cache
from core.viewsets import ThrottledViewSet
import logging
import time
import hashlib
import json

REQUEST_LIMIT = None

class CoursePagination(LimitOffsetPagination):
    default_limit = REQUEST_LIMIT

logger = logging.getLogger(__name__)

def generate_etag(data):
    """Generate an ETag from the data"""
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()

class CourseViewSet(ThrottledViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def list(self, request, *args, **kwargs):
        start_time = time.time()
        cache_time = 0
        db_time = 0
        query_count = 0

        try:
            from django.db import connection, reset_queries
            
            # Enable query logging
            reset_queries()
            
            # Try to get data from cache
            cache_start = time.time()
            data = get_cached_data('courses_data')
            cache_time = (time.time() - cache_start) * 1000

            if data is None:
                # If cache fails, fall back to database
                db_start = time.time()
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
                db_time = (time.time() - db_start) * 1000
                
                # Log query information
                query_count = len(connection.queries)
                queries = connection.queries
                logger.warning(f"Cache miss for courses_data. Executed {query_count} queries:")
                for query in queries:
                    logger.warning(f"Query: {query['sql'][:500]}...")
                    logger.warning(f"Time: {query['time']}")

            # Generate ETag
            etag = quote_etag(generate_etag(data))
            
            # Check if client's ETag matches
            if request.META.get('HTTP_IF_NONE_MATCH') == etag:
                return Response(status=304)
            
            # Handle pagination
            page = self.paginate_queryset(data)
            if page is not None:
                response = self.get_paginated_response(page)
            else:
                response = Response(data)
            
            # Calculate total duration
            total_duration = (time.time() - start_time) * 1000

            # Set response headers
            response['ETag'] = etag
            response['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
            latest_update = Course.objects.aggregate(Max('modified_at'))['modified_at__max']
            if latest_update:
                response['Last-Modified'] = http_date(datetime.timestamp(latest_update))

            # Set Server-Timing header with detailed timing
            timings = [
                f"cache;dur={cache_time:.2f}",
                f"db;dur={db_time:.2f}",
                f"total;dur={total_duration:.2f}",
                f"queries;desc={query_count}"
            ]
            response['Server-Timing'] = ', '.join(timings)
            
            return response
        except Exception as e:
            logger.error(f"Error in CourseViewSet.list: {str(e)}", exc_info=True)
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

    @action(detail=False, methods=['get'])
    def debug(self, request):
        """Debug endpoint to check cache and database timing"""
        try:
            # Get data from cache
            cache_start = time.time()
            cached_data = get_cached_data('courses_data')
            cache_time = (time.time() - cache_start) * 1000
            
            # Get data from database
            db_start = time.time()
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            db_data = serializer.data
            db_time = (time.time() - db_start) * 1000
            
            return Response({
                'cache_hit': cached_data is not None,
                'cache_time_ms': cache_time,
                'db_time_ms': db_time,
                'cached_items': len(cached_data) if cached_data else 0,
                'db_items': len(db_data),
                'data_match': cached_data == db_data if cached_data else False
            })
        except Exception as e:
            logger.error(f"Error in debug endpoint: {str(e)}")
            return Response({"error": str(e)}, status=500)
