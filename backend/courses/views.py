from django.db.models import Q, Max
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer
from rest_framework.pagination import LimitOffsetPagination
from django.utils.http import http_date
from datetime import datetime
from core.cache_utils import get_cached_data

REQUEST_LIMIT = None

# def courses_list(request):
#     courses = Course.objects.all()
#     return render(request, 'courses.html', {'courses': courses})

class CoursePagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('title')
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def list(self, request, *args, **kwargs):
        # Get data from cache
        data = get_cached_data('courses_data')
        
        # Handle pagination
        page = self.paginate_queryset(data)
        if page is not None:
            return self.get_paginated_response(page)
        
        return Response(data)

    def head(self, request, *args, **kwargs):
        latest_update = Course.objects.aggregate(Max('modified_at'))['modified_at__max']
        if latest_update:
            response = Response()
            response['Last-Modified'] = http_date(datetime.timestamp(latest_update))
            return response
        return Response()
