from django.core.cache import cache
from professors.models import Professor
from professors.serializers import ProfessorSerializer
from courses.models import Course
from courses.serializers import CourseSerializer
from professors.models import Department
from professors.serializers import DepartmentSerializer

# Cache for 24 hours
CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours

def warm_cache():
    # Cache professors data
    professors = Professor.objects.all().order_by('empirical_bayes_rank') 
    professors_data = ProfessorSerializer(professors, many=True).data
    cache.set('professors_data', professors_data, CACHE_TIMEOUT)

    # Cache departments data
    departments = Department.objects.all().order_by('name')
    departments_data = DepartmentSerializer(departments, many=True).data
    cache.set('departments_data', departments_data, CACHE_TIMEOUT)

    # Cache courses data
    courses = Course.objects.all().order_by('title')
    courses_data = CourseSerializer(courses, many=True).data
    cache.set('courses_data', courses_data, CACHE_TIMEOUT)

def get_cached_data(key):
    """Get data from cache, if it doesn't exist, warm the cache first"""
    data = cache.get(key)
    if data is None:
        warm_cache()
        data = cache.get(key)
    return data
