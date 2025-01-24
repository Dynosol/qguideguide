from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """Warm up the cache during application startup."""
        from core.cache_utils import warm_cache
        warm_cache()  # This will run during Django startup