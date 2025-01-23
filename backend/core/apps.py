from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """Warm up the cache on the first request."""
        from django.core.signals import request_started
        from core.cache_utils import warm_cache

        def warm_cache_on_first_request(sender, **kwargs):
            warm_cache()
            request_started.disconnect(warm_cache_on_first_request)

        request_started.connect(warm_cache_on_first_request)