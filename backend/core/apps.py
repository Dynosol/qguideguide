from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Called when Django starts. This is where we'll warm up our cache.
        Note: In development with auto-reloader, this runs twice - once for the reloader, once for the actual process.
        """
        # Import here to avoid circular import
        from .cache_utils import warm_cache
        import os
        
        # Only run on main thread (avoid running twice in development)
        if os.environ.get('RUN_MAIN', None) != 'true':
            logger.info("Warming cache on startup...")
            warm_cache()