import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from professors.models import Professor, Department

# Updated process_professors command
class Command(BaseCommand):
    help = 'Process professors.json file and create Professor objects'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to professors.json file')

    def handle(self, *args, **options):
        try:
            file_path = options.get('file') or os.path.join(
                settings.BASE_DIR, 'professors/static/json/professors.json'
            )

            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
                return

            with open(file_path, 'r') as file:
                professors_data = json.load(file)

            Professor.objects.all().delete()
            total = len(professors_data)
            self.stdout.write(f'Processing {total} professors...')

            for i, prof_data in enumerate(professors_data, 1):
                # Validate required fields
                name = prof_data.get('Instructor')
                if not name:  # Skip entries without a name
                    self.stdout.write(
                        self.style.WARNING(f'Skipping professor at index {i} (missing name)')
                    )
                    continue

                # Create professor with validated data
                Professor.objects.create(
                    name=name,
                    departments=prof_data.get('Departments', ''),
                    total_ratings=prof_data.get('Total Ratings', 0),
                    empirical_bayes_average=prof_data.get('EB Score', 0),
                    empirical_bayes_rank=prof_data.get('Global Rank', 0),
                    overall_letter_grade=prof_data.get('Overall Grade', ''),
                    intra_department_metrics=prof_data.get('Department Metrics', '')
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully processed {total} professors'))

        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))