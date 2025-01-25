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
        from threading import Thread
        
        # Only run on main thread (avoid running twice in development)
        if os.environ.get('RUN_MAIN', None) != 'true':
            try:
                # Run cache warming in a separate thread to not block server startup
                thread = Thread(target=warm_cache)
                thread.daemon = True
                thread.start()
                logger.info("Started cache warming thread")
            except Exception as e:
                logger.error(f"Failed to start cache warming thread: {str(e)}")
                # Fallback to synchronous cache warming
                logger.info("Falling back to synchronous cache warming...")
                try:
                    warm_cache()
                except Exception as e:
                    logger.error(f"Failed to warm cache synchronously: {str(e)}")