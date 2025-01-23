from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """Warm up the cache when the application starts"""
        from core.cache_utils import warm_cache
        warm_cache()
