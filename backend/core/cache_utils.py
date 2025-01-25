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
from redis.exceptions import ConnectionError, TimeoutError
from functools import wraps
import backoff

logger = logging.getLogger(__name__)

# Cache for 24 hours
CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours
LOCK_TIMEOUT = 60  # 1 minute lock timeout
MAX_RETRIES = 3

def with_redis_retry(func):
    @wraps(func)
    @backoff.on_exception(backoff.expo,
                         (ConnectionError, TimeoutError),
                         max_tries=MAX_RETRIES)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ConnectionError, TimeoutError) as e:
            logger.error(f"Redis operation failed after {MAX_RETRIES} retries: {str(e)}")
            raise
    return wrapper

@with_redis_retry
def acquire_lock(lock_id):
    """Try to acquire a lock using cache with retry"""
    logger.info(f"Acquiring lock for {lock_id}")
    return cache.add(f"lock_{lock_id}", True, LOCK_TIMEOUT)

@with_redis_retry
def release_lock(lock_id):
    """Release the lock with retry"""
    logger.info(f"Releasing lock for {lock_id}")
    cache.delete(f"lock_{lock_id}")

@with_redis_retry
def set_cache_data(key, data):
    """Set cache data with retry"""
    logger.info(f"Setting cache data for {key}")
    cache.set(key, data, CACHE_TIMEOUT)
    
def warm_cache():
    """Warm up the cache with all necessary data"""
    # Try to acquire lock
    try:
        if not acquire_lock("cache_warming"):
            logger.info("Another process is warming the cache, skipping...")
            return

        logger.info("Starting cache warming process...")
        start_time = time.time()

        success = True
        # Use atomic transaction to ensure consistency
        with transaction.atomic():
            try:
                # Cache courses data
                logger.info("Caching courses...")
                courses = Course.objects.select_related().all().order_by('title')
                logger.info(f"Found {len(courses)} courses")
                courses_data = CourseSerializer(courses, many=True).data
                set_cache_data('courses_data', courses_data)

                # Cache professors data
                logger.info("Caching professors...")
                professors = Professor.objects.select_related().all().order_by('empirical_bayes_rank')
                logger.info(f"Found {len(professors)} professors")
                professors_data = ProfessorSerializer(professors, many=True).data
                set_cache_data('professors_data', professors_data)

                # Cache departments data
                logger.info("Caching departments...")
                departments = Department.objects.select_related().all().order_by('name')
                logger.info(f"Found {len(departments)} departments")
                departments_data = DepartmentSerializer(departments, many=True).data
                set_cache_data('departments_data', departments_data)

            except Exception as e:
                success = False
                logger.error(f"Error during cache warming: {str(e)}")
                raise

        if success:
            # Only set these flags if everything succeeded
            set_cache_data('cache_warmed', True)
            set_cache_data('last_cache_update', time.time())
            logger.info(f"Cache warming completed successfully in {time.time() - start_time:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Cache warming failed: {str(e)}")
        # Don't set empty lists anymore, let it fall back to database
    finally:
        try:
            release_lock("cache_warming")
        except Exception as e:
            logger.error(f"Error releasing cache lock: {str(e)}")

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
                    set_cache_data(key, data)
                    logger.info(f"Cached {len(data)} items for {key}")
        
        return data
    except Exception as e:
        logger.error(f"Error getting cached data for {key}: {str(e)}")
        return []
