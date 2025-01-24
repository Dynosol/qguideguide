from django.db.models import Q, Max
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
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
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_queryset(self):
        """Return an optimized queryset"""
        if self.action == 'list':
            return Course.objects.only(
                'id', 'title', 'department', 'instructor', 'term',
                'course_mean_rating', 'responses'
            ).order_by('title')
        return Course.objects.all()

    def get_serializer_class(self):
        """Return different serializers for list and detail"""
        if self.action == 'list':
            return CourseListSerializer
        return CourseSerializer

    def list(self, request, *args, **kwargs):
        start_time = time.time()
        cache_time = 0
        db_time = 0
        query_count = 0

        try:
            from django.db import connection, reset_queries
            import json
            
            # Enable query logging
            reset_queries()
            
            # Try to get data from cache
            cache_start = time.time()
            data = get_cached_data('courses_list_data')
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
                logger.warning(f"Cache miss for courses_list_data. Executed {query_count} queries:")
                for query in queries:
                    logger.warning(f"Query: {query['sql'][:500]}...")
                    logger.warning(f"Time: {query['time']}")
            
            # Handle pagination
            page = self.paginate_queryset(data)
            if page is not None:
                response = self.get_paginated_response(page)
            else:
                response = Response(data)
            
            # Calculate total duration
            total_duration = (time.time() - start_time) * 1000

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
        """Diagnostic endpoint to help debug performance issues"""
        try:
            from django.db import connection
            from django.core.cache import cache
            import json

            # Test cache
            cache_start = time.time()
            cache_test = cache.set('test_key', 'test_value', 10)
            cache_get = cache.get('test_key')
            cache_time = (time.time() - cache_start) * 1000

            # Test database
            db_start = time.time()
            test_query = Course.objects.all()[:1]
            list(test_query)  # Execute the query
            db_time = (time.time() - db_start) * 1000

            # Get cache stats
            cache_keys = {
                'courses_list_data': cache.get('courses_list_data') is not None,
                'courses_data': cache.get('courses_data') is not None,
                'professors_data': cache.get('professors_data') is not None,
                'departments_data': cache.get('departments_data') is not None,
            }

            return Response({
                'cache': {
                    'working': cache_test and cache_get == 'test_value',
                    'time_ms': cache_time,
                    'keys_present': cache_keys
                },
                'database': {
                    'time_ms': db_time,
                    'backend': connection.vendor,
                    'queries_executed': len(connection.queries)
                }
            })
        except Exception as e:
            logger.error(f"Error in diagnostic endpoint: {str(e)}", exc_info=True)
            return Response({"error": str(e)}, status=500)
