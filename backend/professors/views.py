from django.shortcuts import render
from rest_framework import viewsets, pagination, filters
from rest_framework_datatables import filters as dt_filters
from .models import Professor, Department
from rest_framework.pagination import LimitOffsetPagination
from .serializers import ProfessorSerializer, DepartmentSerializer
from django.utils.http import http_date, quote_etag
from django.db.models import Max
from datetime import datetime
from rest_framework.response import Response
from core.cache_utils import get_cached_data
from core.viewsets import ThrottledViewSet
import logging
import hashlib
import json

logger = logging.getLogger(__name__)

REQUEST_LIMIT = None

class ProfessorPagination(LimitOffsetPagination):
    default_limit = REQUEST_LIMIT  # Number of records per page

def generate_etag(data):
    """Generate an ETag from the data"""
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()

class ProfessorViewSet(ThrottledViewSet):
    queryset = Professor.objects.all().order_by('empirical_bayes_rank')
    serializer_class = ProfessorSerializer
    pagination_class = ProfessorPagination

    def list(self, request, *args, **kwargs):
        try:
            # Get data from cache
            data = get_cached_data('professors_data')
            if data is None:
                # If cache completely fails, fall back to database
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data

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

            # Set cache headers
            response['ETag'] = etag
            response['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
            latest_update = Professor.objects.aggregate(Max('modified_at'))['modified_at__max']
            if latest_update:
                response['Last-Modified'] = http_date(datetime.timestamp(latest_update))
            
            return response
        except Exception as e:
            logger.error(f"Error in ProfessorViewSet.list: {str(e)}")
            return Response(
                {"error": "An error occurred while fetching professors"},
                status=500
            )

    def head(self, request, *args, **kwargs):
        try:
            # Check permissions first
            self.check_permissions(request)
            
            latest_update = Professor.objects.aggregate(Max('modified_at'))['modified_at__max']
            response = Response()
            if latest_update:
                response['Last-Modified'] = http_date(datetime.timestamp(latest_update))
            return response
        except Exception as e:
            logger.error(f"Error in ProfessorViewSet.head: {str(e)}")
            return Response(status=500)

class DepartmentViewSet(ThrottledViewSet):
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    pagination_class = ProfessorPagination

    def list(self, request, *args, **kwargs):
        try:
            # Get data from cache
            data = get_cached_data('departments_data')
            if data is None:
                # If cache completely fails, fall back to database
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data

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

            # Set cache headers
            response['ETag'] = etag
            response['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
            latest_update = Department.objects.aggregate(Max('modified_at'))['modified_at__max']
            if latest_update:
                response['Last-Modified'] = http_date(datetime.timestamp(latest_update))
            
            return response
        except Exception as e:
            logger.error(f"Error in DepartmentViewSet.list: {str(e)}")
            return Response(
                {"error": "An error occurred while fetching departments"},
                status=500
            )

    def head(self, request, *args, **kwargs):
        try:
            # Check permissions first
            self.check_permissions(request)
            
            latest_update = Department.objects.aggregate(Max('modified_at'))['modified_at__max']
            response = Response()
            if latest_update:
                response['Last-Modified'] = http_date(datetime.timestamp(latest_update))
            return response
        except Exception as e:
            logger.error(f"Error in DepartmentViewSet.head: {str(e)}")
            return Response(status=500)
