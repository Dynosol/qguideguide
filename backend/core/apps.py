from django.apps import AppConfig
from django.db.migrations.executor import MigrationExecutor
from django.db import connections

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """Warm up the cache during application startup, but only after migrations."""
        # Skip cache warming during migrations
        connection = connections['default']
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if not plan:  # No migrations needed
            from core.cache_utils import warm_cache
            warm_cache()  # Only warm cache if no migrations pending