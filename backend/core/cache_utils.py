from django.core.cache import cache
from professors.models import Professor, Department
from courses.models import Course
from professors.serializers import ProfessorSerializer, DepartmentSerializer
from courses.serializers import CourseSerializer
from django.conf import settings

# Cache for 1 hour by default
CACHE_TIMEOUT = 3600

def warm_cache():
    """Warm up the cache with all necessary data"""
    # Cache professors data
    professors = Professor.objects.all().order_by('empirical_bayes_rank')
    professors_data = ProfessorSerializer(professors, many=True).data
    cache.set('professors_data', professors_data, timeout=CACHE_TIMEOUT)

    # Cache departments data
    departments = Department.objects.all().order_by('name')
    departments_data = DepartmentSerializer(departments, many=True).data
    cache.set('departments_data', departments_data, timeout=CACHE_TIMEOUT)

    # Cache courses data
    courses = Course.objects.all().order_by('title')
    courses_data = CourseSerializer(courses, many=True).data
    cache.set('courses_data', courses_data, timeout=CACHE_TIMEOUT)

def get_cached_data(key):
    """Get data from cache, if missing rebuild cache and return data"""
    data = cache.get(key)
    if data is None:
        warm_cache()
        data = cache.get(key)
    return data
