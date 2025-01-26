from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.db import connection

class Command(BaseCommand):
    help = 'Fix duplicate content types'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Find duplicates
            cursor.execute("""
                SELECT app_label, model, COUNT(*)
                FROM django_content_type
                GROUP BY app_label, model
                HAVING COUNT(*) > 1
            """)
            duplicates = cursor.fetchall()

            for app_label, model, count in duplicates:
                self.stdout.write(f'Fixing {count} duplicates for {app_label}.{model}')
                # Keep the first one, delete others
                content_types = ContentType.objects.filter(
                    app_label=app_label,
                    model=model
                ).order_by('id')
                
                first = content_types.first()
                if first:
                    content_types.exclude(id=first.id).delete()

        self.stdout.write(self.style.SUCCESS('Successfully fixed content types'))
