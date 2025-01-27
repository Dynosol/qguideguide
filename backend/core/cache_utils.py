from django.core.cache import cache
import logging
import time
from django.db import transaction
from redis.exceptions import ConnectionError, TimeoutError
from functools import wraps
import backoff
import zlib
import json
from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger(__name__)

# Cache settings
CACHE_TIMEOUT = 60 * 60 * 24
LOCK_TIMEOUT = 60
MAX_RETRIES = 3

class LazyLoader:
    """Lazy loader for models and serializers to avoid circular imports"""
    _course_model = None
    _professor_model = None
    _department_model = None
    _course_serializer = None
    _professor_serializer = None
    _department_serializer = None

    @property
    def Course(self):
        if not self._course_model:
            from courses.models import Course
            self._course_model = Course
        return self._course_model

    @property
    def Professor(self):
        if not self._professor_model:
            from professors.models import Professor
            self._professor_model = Professor
        return self._professor_model

    @property
    def Department(self):
        if not self._department_model:
            from professors.models import Department
            self._department_model = Department
        return self._department_model

    @property
    def CourseSerializer(self):
        if not self._course_serializer:
            from courses.serializers import CourseSerializer
            self._course_serializer = CourseSerializer
        return self._course_serializer

    @property
    def ProfessorSerializer(self):
        if not self._professor_serializer:
            from professors.serializers import ProfessorSerializer
            self._professor_serializer = ProfessorSerializer
        return self._professor_serializer

    @property
    def DepartmentSerializer(self):
        if not self._department_serializer:
            from professors.serializers import DepartmentSerializer
            self._department_serializer = DepartmentSerializer
        return self._department_serializer

# Create global lazy loader instance
lazy = LazyLoader()

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
    """Warm up the cache with all necessary data"""
    try:
        if not acquire_lock("cache_warming"):
            logger.info("Another process is warming the cache, skipping...")
            return

        logger.info("Starting cache warming process...")
        start_time = time.time()
        cache.set('cache_warming_in_progress', True, LOCK_TIMEOUT)

        with transaction.atomic():
            try:
                def cache_with_compression(model, serializer_class, cache_key, chunk_size=100):
                    all_data = []
                    for chunk in model.objects.iterator(chunk_size=chunk_size):
                        chunk_data = serializer_class(chunk).data
                        all_data.append(chunk_data)
                        
                    # Compress the data before caching
                    json_data = json.dumps(all_data, cls=DjangoJSONEncoder)
                    compressed = zlib.compress(json_data.encode('utf-8'))
                    set_cache_data(f'compressed_{cache_key}', compressed)
                    logger.info(f"Cached and compressed {len(all_data)} records for {cache_key}")

                # Cache data with compression
                cache_with_compression(lazy.Course, lazy.CourseSerializer, 'courses_data', chunk_size=1000)
                cache_with_compression(lazy.Professor, lazy.ProfessorSerializer, 'professors_data', chunk_size=1000)
                
                departments = lazy.Department.objects.select_related().all()
                departments_data = lazy.DepartmentSerializer(departments, many=True).data
                set_cache_data('departments_data', departments_data)

            except Exception as e:
                logger.error(f"Error during cache warming: {str(e)}")
                raise

        set_cache_data('cache_warmed', True)
        set_cache_data('last_cache_update', time.time())
        logger.info(f"Cache warming completed in {time.time() - start_time:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Error during cache warming: {str(e)}")
        raise
    finally:
        cache.delete('cache_warming_in_progress')
        release_lock("cache_warming")

def get_cached_data(key):
    """Get data from cache with lazy loading fallback"""
    try:
        logger.info(f"Getting cached data for {key}")
        data = cache.get(key)
        
        if data is None and not cache.get('cache_warmed'):
            if is_cache_warming():
                logger.info("Cache is being warmed, waiting...")
                time.sleep(0.5)
                data = cache.get(key)
            else:
                logger.warning(f"Cache miss for {key}, warming cache...")
                warm_cache()
                data = cache.get(key)

        if data is None:
            logger.warning(f"Cache miss for {key} after warming attempt")
            with transaction.atomic():
                chunk_size = 100
                all_data = []
                
                if key == 'courses_data':
                    chunk_size = 50
                    for chunk in lazy.Course.objects.select_related().iterator(chunk_size=chunk_size):
                        all_data.append(lazy.CourseSerializer(chunk).data)
                elif key == 'professors_data':
                    for chunk in lazy.Professor.objects.select_related().iterator(chunk_size=chunk_size):
                        all_data.append(lazy.ProfessorSerializer(chunk).data)
                elif key == 'departments_data':
                    departments = lazy.Department.objects.select_related().all()
                    all_data = lazy.DepartmentSerializer(departments, many=True).data
                
                if all_data:
                    set_cache_data(key, all_data)
                    data = all_data

        return data or []
    except Exception as e:
        logger.error(f"Error getting cached data for {key}: {str(e)}")
        return []
