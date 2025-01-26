# wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django FIRST
application = get_wsgi_application()

# Import and run cache warming AFTER initialization
from core.cache_utils import warm_cache
import threading

def warm_cache_async():
    warm_cache()

# Start cache warming thread
threading.Thread(target=warm_cache_async).start()