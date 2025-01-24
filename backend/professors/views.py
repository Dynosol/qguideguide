from django.shortcuts import render
from rest_framework import viewsets, pagination
from .models import Professor, Department
from rest_framework.pagination import LimitOffsetPagination
from .serializers import ProfessorSerializer, DepartmentSerializer
from django.utils.http import http_date
from django.db.models import Max
from datetime import datetime
from rest_framework.response import Response
from core.cache_utils import get_cached_data
import logging

logger = logging.getLogger(__name__)

REQUEST_LIMIT = None

class ProfessorPagination(LimitOffsetPagination):
    default_limit = REQUEST_LIMIT  # Number of records per page

class ProfessorViewSet(viewsets.ModelViewSet):
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

            # Handle pagination
            page = self.paginate_queryset(data)
            if page is not None:
                return self.get_paginated_response(page)
            
            return Response(data)
        except Exception as e:
            logger.error(f"Error in ProfessorViewSet.list: {str(e)}")
            return Response(
                {"error": "An error occurred while fetching professors"},
                status=500
            )

    def head(self, request, *args, **kwargs):
        try:
            latest_update = Professor.objects.aggregate(Max('modified_at'))['modified_at__max']
            if latest_update:
                response = Response()
                response['Last-Modified'] = http_date(datetime.timestamp(latest_update))
                return response
            return Response()
        except Exception as e:
            logger.error(f"Error in ProfessorViewSet.head: {str(e)}")
            return Response(status=500)

class DepartmentViewSet(viewsets.ModelViewSet):
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

            # Handle pagination
            page = self.paginate_queryset(data)
            if page is not None:
                return self.get_paginated_response(page)
            
            return Response(data)
        except Exception as e:
            logger.error(f"Error in DepartmentViewSet.list: {str(e)}")
            return Response(
                {"error": "An error occurred while fetching departments"},
                status=500
            )

    # Mirror ProfessorViewSet's head method
    def head(self, request, *args, **kwargs):
        try:
            latest_update = Department.objects.aggregate(Max('modified_at'))['modified_at__max']
            if latest_update:
                response = Response()
                response['Last-Modified'] = http_date(datetime.timestamp(latest_update))
                return response
            return Response()
        except Exception as e:
            logger.error(f"Error in DepartmentViewSet.head: {str(e)}")
            return Response(status=500)
