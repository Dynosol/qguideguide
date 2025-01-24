#!/usr/bin/env python
import os
import sys
import django

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.cache import cache
import logging
from professors.models import Professor, Department
from professors.serializers import ProfessorSerializer, DepartmentSerializer
from courses.models import Course
from courses.serializers import CourseSerializer, CourseListSerializer

# Cache for 24 hours
CACHE_TIMEOUT = 60 * 60 * 24

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def warm_cache():
    """Warm up the cache independently of Django startup"""
    logger.info("Starting deployment cache warming process...")
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

        logger.info("Deployment cache warming completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error during deployment cache warming: {str(e)}")
        sys.exit(1)  # Exit with error code

if __name__ == '__main__':
    warm_cache()
