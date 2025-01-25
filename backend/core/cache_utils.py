from django.core.cache import cache
from professors.models import Professor
from professors.serializers import ProfessorSerializer
from courses.models import Course
from courses.serializers import CourseSerializer
from professors.models import Department
from professors.serializers import DepartmentSerializer
import logging
import time

logger = logging.getLogger(__name__)

# Cache for 24 hours
CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours
LOCK_TIMEOUT = 60  # 1 minute lock timeout

def acquire_lock(lock_id):
    """Try to acquire a lock using cache"""
    return cache.add(f"lock_{lock_id}", True, LOCK_TIMEOUT)

def release_lock(lock_id):
    """Release the lock"""
    cache.delete(f"lock_{lock_id}")

def warm_cache():
    """Warm up the cache with all necessary data"""
    # Try to acquire lock
    if not acquire_lock("cache_warming"):
        logger.info("Another process is warming the cache, skipping...")
        return

    try:
        logger.info("Starting cache warming process...")
        start_time = time.time()

        # Cache courses data with optimized query
        courses = Course.objects.all().select_related().only(
            'id', 'title', 'department', 'instructor', 'term',
            'subject', 'responses', 'course_mean_rating',
            'materials_mean_rating', 'assignments_mean_rating',
            'feedback_mean_rating', 'section_mean_rating',
            'instructor_mean_rating'
        ).order_by('-course_mean_rating')
        courses_data = CourseSerializer(courses, many=True).data
        cache.set('courses_data', courses_data, CACHE_TIMEOUT)
        logger.info(f"Cached {len(courses_data)} courses in {time.time() - start_time:.2f} seconds")

        # Cache professors data with optimized query
        professors = Professor.objects.all().only(
            'id', 'name', 'departments', 'empirical_bayes_rank',
            'total_ratings', 'empirical_bayes_average'
        ).order_by('empirical_bayes_rank')
        professors_data = ProfessorSerializer(professors, many=True).data
        cache.set('professors_data', professors_data, CACHE_TIMEOUT)
        logger.info(f"Cached {len(professors_data)} professors")

        # Cache departments data with optimized query
        departments = Department.objects.all().only(
            'id', 'name', 'professor_count', 'empirical_bayes_average'
        ).order_by('name')
        departments_data = DepartmentSerializer(departments, many=True).data
        cache.set('departments_data', departments_data, CACHE_TIMEOUT)
        logger.info(f"Cached {len(departments_data)} departments")

        logger.info(f"Cache warming completed in {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error warming cache: {str(e)}")
        # Set empty lists as fallback
        cache.set('courses_data', [], CACHE_TIMEOUT)
        cache.set('professors_data', [], CACHE_TIMEOUT)
        cache.set('departments_data', [], CACHE_TIMEOUT)
    finally:
        release_lock("cache_warming")

def get_cached_data(key):
    """Get data from cache, if it doesn't exist or fails, fall back to database"""
    try:
        data = cache.get(key)
        if data is None:
            logger.warning(f"Cache miss for key: {key}")
            # Don't warm the entire cache, just get the specific data needed
            if key == 'courses_data':
                courses = Course.objects.all().order_by('title')
                data = CourseSerializer(courses, many=True).data
                cache.set(key, data, CACHE_TIMEOUT)
            elif key == 'professors_data':
                professors = Professor.objects.all().order_by('empirical_bayes_rank')
                data = ProfessorSerializer(professors, many=True).data
                cache.set(key, data, CACHE_TIMEOUT)
            elif key == 'departments_data':
                try:
                    departments = Department.objects.all().order_by('name')
                    data = DepartmentSerializer(departments, many=True).data
                    cache.set(key, data, CACHE_TIMEOUT)
                except Exception as dept_error:
                    logger.warning(f"Error getting departments data: {str(dept_error)}")
                    data = []
        return data
    except Exception as e:
        logger.error(f"Error getting cached data for {key}: {str(e)}")
        return None
