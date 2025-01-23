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

REQUEST_LIMIT = None

class ProfessorPagination(LimitOffsetPagination):
    default_limit = REQUEST_LIMIT  # Number of records per page

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all().order_by('empirical_bayes_rank')
    serializer_class = ProfessorSerializer
    pagination_class = ProfessorPagination

    def list(self, request, *args, **kwargs):
        # Get data from cache
        data = get_cached_data('professors_data')
        
        # Handle pagination
        page = self.paginate_queryset(data)
        if page is not None:
            return self.get_paginated_response(page)
        
        return Response(data)

    def head(self, request, *args, **kwargs):
        latest_update = Professor.objects.aggregate(Max('modified_at'))['modified_at__max']
        response = Response(None, status=200)
        if latest_update:
            response['Last-Modified'] = http_date(latest_update.timestamp())
        return response

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    pagination_class = ProfessorPagination

    def list(self, request, *args, **kwargs):
        data = get_cached_data('departments_data')
        response = self.get_paginated_response(data) if self.paginate_queryset(data) else Response(data)
        return response

    def head(self, request, *args, **kwargs):
        """Mirror ProfessorViewSet's head method"""
        latest_update = Department.objects.aggregate(Max('modified_at'))['modified_at__max']
        response = Response(status=200)
        if latest_update:
            response['Last-Modified'] = http_date(latest_update.timestamp())
        return response
