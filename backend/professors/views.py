from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_datatables import filters as dt_filters
from .models import Professor, Department
from rest_framework.pagination import LimitOffsetPagination
from .serializers import ProfessorSerializer, DepartmentSerializer
from django.utils.http import http_date, quote_etag
from django.db.models import Max
from datetime import datetime
from core.cache_utils import cache
from core.viewsets import ThrottledViewSet
import hashlib
import json

REQUEST_LIMIT = None

class ProfessorPagination(LimitOffsetPagination):
    default_limit = REQUEST_LIMIT

def generate_etag(data):
    """Generate an ETag from the data"""
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()

class ProfessorViewSet(ThrottledViewSet):
    queryset = Professor.objects.all().order_by('empirical_bayes_rank')
    serializer_class = ProfessorSerializer
    pagination_class = ProfessorPagination

    def list(self, request, *args, **kwargs):
        cache_key = 'professors_list'
        data = cache.get(cache_key)
        
        if data is None:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = self.get_paginated_response(serializer.data).data
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
            
            cache.set(cache_key, data, timeout=86400)
        
        return Response(data)

class DepartmentViewSet(ThrottledViewSet):
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    pagination_class = ProfessorPagination

    def list(self, request, *args, **kwargs):
        cache_key = 'departments_list'
        data = cache.get(cache_key)
        
        if data is None:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = self.get_paginated_response(serializer.data).data
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
            
            cache.set(cache_key, data, timeout=86400)
        
        return Response(data)