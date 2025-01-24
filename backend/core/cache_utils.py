from django.core.cache import cache
from professors.models import Professor
from professors.serializers import ProfessorSerializer
from courses.models import Course
from courses.serializers import CourseSerializer, CourseListSerializer
from professors.models import Department
from professors.serializers import DepartmentSerializer
import logging

logger = logging.getLogger(__name__)

# Cache for 24 hours
CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours

def warm_cache():
    """Warm up the cache with all necessary data"""
    logger.info("Starting cache warming process...")
    try:
        # Cache professors data
        professors = Professor.objects.all().order_by('empirical_bayes_rank')
        professors_data = ProfessorSerializer(professors, many=True).data
        cache.set('professors_data', professors_data, CACHE_TIMEOUT)
        logger.info(f"Cached {len(professors_data)} professors")

        # Cache departments data
        departments = Department.objects.all().order_by('name')
        departments_data = DepartmentSerializer(departments, many=True).data
        cache.set('departments_data', departments_data, CACHE_TIMEOUT)
        logger.info(f"Cached {len(departments_data)} departments")

        # Cache courses data (both full and list views)
        courses = Course.objects.all().order_by('title')
        courses_full_data = CourseSerializer(courses, many=True).data
        courses_list_data = CourseListSerializer(courses, many=True).data
        
        cache.set('courses_data', courses_full_data, CACHE_TIMEOUT)
        cache.set('courses_list_data', courses_list_data, CACHE_TIMEOUT)
        
        logger.info(f"Cached {len(courses_full_data)} courses (full data)")
        logger.info(f"Cached {len(courses_list_data)} courses (list data)")

        logger.info("Cache warming completed successfully")
    except Exception as e:
        logger.error(f"Error during cache warming: {str(e)}")
        raise

def get_cached_data(key):
    """Get data from cache, if it doesn't exist or fails, fall back to database"""
    try:
        data = cache.get(key)
        if data is None:
            logger.warning(f"Cache miss for key: {key}")
            # Don't warm the entire cache, just get the specific data needed
            if key == 'courses_list_data':
                courses = Course.objects.all().order_by('title')
                data = CourseListSerializer(courses, many=True).data
                cache.set(key, data, CACHE_TIMEOUT)
            elif key == 'courses_data':
                courses = Course.objects.all().order_by('title')
                data = CourseSerializer(courses, many=True).data
                cache.set(key, data, CACHE_TIMEOUT)
            elif key == 'professors_data':
                professors = Professor.objects.all().order_by('empirical_bayes_rank')
                data = ProfessorSerializer(professors, many=True).data
                cache.set(key, data, CACHE_TIMEOUT)
            elif key == 'departments_data':
                departments = Department.objects.all().order_by('name')
                data = DepartmentSerializer(departments, many=True).data
                cache.set(key, data, CACHE_TIMEOUT)
            logger.info(f"Generated and cached new data for key: {key}")
        return data
    except Exception as e:
        logger.error(f"Error getting cached data for key {key}: {str(e)}")
        return None
