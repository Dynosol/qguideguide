from rest_framework import viewsets
from rest_framework.response import Response
from .models import Professor, Department
from .serializers import ProfessorSerializer, DepartmentSerializer
from core.cache_utils import get_cached_data
from django.db import connection

class ProfessorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Professor.objects.all().order_by('empirical_bayes_rank')
    serializer_class = ProfessorSerializer
    pagination_class = None  # Disable pagination for full dataset caching

    def list(self, request, *args, **kwargs):
        try:
            data = get_cached_data('professors_data')
            return Response(data)
        except Exception as e:
            connection.ensure_connection()
            try:
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            finally:
                connection.close()

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    pagination_class = None  # Disable pagination for full dataset caching

    def list(self, request, *args, **kwargs):
        try:
            data = get_cached_data('departments_data')
            return Response(data)
        except Exception as e:
            connection.ensure_connection()
            try:
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            finally:
                connection.close()