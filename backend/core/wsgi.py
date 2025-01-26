"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from core.cache_utils import warm_cache
import threading

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

# Warm the cache in a separate thread to not block server startup
def warm_cache_async():
    warm_cache()

threading.Thread(target=warm_cache_async).start()
