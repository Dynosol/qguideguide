from django.core.cache import cache
from professors.models import Professor
from professors.serializers import ProfessorSerializer
from courses.models import Course
from courses.serializers import CourseSerializer
from professors.models import Department
from professors.serializers import DepartmentSerializer
from django.db.models import Prefetch
import logging
import time
from django.db import transaction

logger = logging.getLogger(__name__)

# Cache for 24 hours
CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours
LOCK_TIMEOUT = 60  # 1 minute lock timeout

def acquire_lock(lock_id):
    """Try to acquire a lock using cache"""
    logger.info(f"Acquiring lock for {lock_id}")
    return cache.add(f"lock_{lock_id}", True, LOCK_TIMEOUT)

def release_lock(lock_id):
    """Release the lock"""
    logger.info(f"Releasing lock for {lock_id}")
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

        # Use atomic transaction to ensure consistency
        with transaction.atomic():
            # Cache courses data with optimized query
            logger.info("Caching courses...")
            courses = Course.objects.select_related().all().order_by('title')
            logger.info(f"Found {len(courses)} courses")
            courses_data = CourseSerializer(courses, many=True).data
            cache.set('courses_data', courses_data, CACHE_TIMEOUT)
            logger.info(f"Cached {len(courses_data)} courses")

            # Cache professors data with optimized query
            logger.info("Caching professors...")
            professors = Professor.objects.select_related().all().order_by('empirical_bayes_rank')
            logger.info(f"Found {len(professors)} professors")
            professors_data = ProfessorSerializer(professors, many=True).data
            cache.set('professors_data', professors_data, CACHE_TIMEOUT)
            logger.info(f"Cached {len(professors_data)} professors")

            # Cache departments data with optimized query
            logger.info("Caching departments...")
            departments = Department.objects.select_related().all().order_by('name')
            logger.info(f"Found {len(departments)} departments")
            departments_data = DepartmentSerializer(departments, many=True).data
            cache.set('departments_data', departments_data, CACHE_TIMEOUT)
            logger.info(f"Cached {len(departments_data)} departments")

            # Set a flag indicating cache is warm
            cache.set('cache_warmed', True, CACHE_TIMEOUT)
            cache.set('last_cache_update', time.time(), CACHE_TIMEOUT)

        logger.info(f"Cache warming completed in {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error warming cache: {str(e)}")
        # Set empty lists as fallback
        cache.set('courses_data', [], CACHE_TIMEOUT)
        cache.set('professors_data', [], CACHE_TIMEOUT)
        cache.set('departments_data', [], CACHE_TIMEOUT)
        cache.set('cache_warmed', False, CACHE_TIMEOUT)
    finally:
        release_lock("cache_warming")

def get_cached_data(key):
    """Get data from cache, if it doesn't exist or fails, fall back to database"""
    try:
        logger.info(f"Getting cached data for {key}")
        data = cache.get(key)
        
        # If cache is cold or data is missing, try to warm it
        if data is None and not cache.get('cache_warmed'):
            logger.warning(f"Cache miss for {key} and cache is cold. Warming cache...")
            warm_cache()
            data = cache.get(key)

        # If still no data after warming, fall back to database
        if data is None:
            logger.warning(f"Cache miss for {key} after warming attempt")
            with transaction.atomic():
                if key == 'courses_data':
                    logger.info("Getting courses data from database")
                    courses = Course.objects.select_related().all().order_by('title')
                    data = CourseSerializer(courses, many=True).data
                elif key == 'professors_data':
                    logger.info("Getting professors data from database")
                    professors = Professor.objects.select_related().all().order_by('empirical_bayes_rank')
                    data = ProfessorSerializer(professors, many=True).data
                elif key == 'departments_data':
                    logger.info("Getting departments data from database")
                    departments = Department.objects.select_related().all().order_by('name')
                    data = DepartmentSerializer(departments, many=True).data
                
                if data:
                    cache.set(key, data, CACHE_TIMEOUT)
                    logger.info(f"Cached {len(data)} items for {key}")
        
        return data
    except Exception as e:
        logger.error(f"Error getting cached data for {key}: {str(e)}")
        return []
