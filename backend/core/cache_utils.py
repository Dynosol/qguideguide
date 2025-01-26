from django.core.cache import cache
from professors.serializers import ProfessorSerializer
from courses.serializers import CourseSerializer
from professors.serializers import DepartmentSerializer
from django.db.models import Prefetch
import logging
import time
from django.db import transaction
from redis.exceptions import ConnectionError, TimeoutError
from functools import wraps
import backoff
import os

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
    
def is_cache_warming():
    """Check if cache is currently being warmed"""
    return cache.get('cache_warming_in_progress', False)

def warm_cache():
    from courses.models import Course
    from professors.models import Professor, Department
    """Warm up the cache with all necessary data"""
    # Try to acquire lock
    try:
        if not acquire_lock("cache_warming"):
            logger.info("Another process is warming the cache, skipping...")
            return

        logger.info("Starting cache warming process...")
        start_time = time.time()

        # Set warming in progress flag
        cache.set('cache_warming_in_progress', True, LOCK_TIMEOUT)

        success = True
        # Use atomic transaction to ensure consistency
        with transaction.atomic():
            try:
                # Cache in chunks to reduce memory usage
                def cache_in_chunks(model, serializer_class, cache_key, chunk_size=100):
                    total = model.objects.count()
                    chunks = (total // chunk_size) + (1 if total % chunk_size else 0)
                    
                    all_data = []
                    for i in range(chunks):
                        offset = i * chunk_size
                        chunk = model.objects.select_related().all().order_by('id')[offset:offset + chunk_size]
                        chunk_data = serializer_class(chunk, many=True).data
                        all_data.extend(chunk_data)
                        logger.info(f"Cached chunk {i+1}/{chunks} for {cache_key}")
                    
                    set_cache_data(cache_key, all_data)
                    logger.info(f"Finished caching {total} items for {cache_key}")

                # Cache courses data in chunks
                logger.info("Caching courses...")
                cache_in_chunks(Course, CourseSerializer, 'courses_data', chunk_size=50)

                # Cache professors data in chunks
                logger.info("Caching professors...")
                cache_in_chunks(Professor, ProfessorSerializer, 'professors_data', chunk_size=100)

                # Cache departments data (usually small enough to do at once)
                logger.info("Caching departments...")
                departments = Department.objects.select_related().all().order_by('name')
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
        logger.error(f"Error during cache warming: {str(e)}")
        raise
    finally:
        # Always clear the warming in progress flag and release lock
        cache.delete('cache_warming_in_progress')
        release_lock("cache_warming")

def get_cached_data(cache_key):
    """
    Thread-safe function to get data from cache
    """
    try:
        return cache.get(cache_key)
    except Exception as e:
        # Log the error but don't raise it - let the view fall back to database
        print(f"Cache error in get_cached_data for key {cache_key}: {str(e)}")
        return None

def get_cached_data(key):
    """Get data from cache, if it doesn't exist or fails, fall back to database"""
    try:
        logger.info(f"Getting cached data for {key}")
        data = cache.get(key)
        
        # If cache is cold or data is missing, try to warm it
        if data is None and not cache.get('cache_warmed'):
            # Check if cache is already being warmed
            if is_cache_warming():
                logger.info("Cache is currently being warmed, waiting for data...")
                # Wait for a short time and try again
                time.sleep(0.5)
                data = cache.get(key)
            else:
                logger.warning(f"Cache miss for {key} and cache is cold. Warming cache...")
                warm_cache()
                data = cache.get(key)

        # If still no data after warming, fall back to database with chunking
        if data is None:
            logger.warning(f"Cache miss for {key} after warming attempt")
            with transaction.atomic():
                chunk_size = 100  # Default chunk size
                all_data = []
                
                if key == 'courses_data':
                    from courses.models import Course
                    chunk_size = 50  # Smaller chunks for courses due to size
                    for chunk in Course.objects.select_related().all().order_by('title').iterator(chunk_size=chunk_size):
                        all_data.append(CourseSerializer(chunk).data)
                elif key == 'professors_data':
                    from professors.models import Professor
                    for chunk in Professor.objects.select_related().all().order_by('empirical_bayes_rank').iterator(chunk_size=chunk_size):
                        all_data.append(ProfessorSerializer(chunk).data)
                elif key == 'departments_data':
                    from professors.models import Department
                    departments = Department.objects.select_related().all().order_by('name')
                    all_data = DepartmentSerializer(departments, many=True).data
                
                if all_data:
                    set_cache_data(key, all_data)
                    logger.info(f"Cached {len(all_data)} items for {key}")
                    data = all_data

        return data or []
    except Exception as e:
        logger.error(f"Error getting cached data for {key}: {str(e)}")
        return []
