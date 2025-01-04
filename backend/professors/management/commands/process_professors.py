import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from professors.models import Professor, Department

class Command(BaseCommand):
    help = 'Process professors.json file and create Professor objects'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to professors.json file')

    def handle(self, *args, **options):
        try:
            # Get file path from arguments or use default
            file_path = options.get('file')
            if not file_path:
                file_path = os.path.join(settings.BASE_DIR, 'professors/static/json/professors.json')

            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
                return

            with open(file_path, 'r') as file:
                professors_data = json.load(file)

            # Clear existing professors
            Professor.objects.all().delete()

            # Track progress
            total = len(professors_data)
            self.stdout.write(f'Processing {total} professors...')

            for i, prof_data in enumerate(professors_data, 1):
                if i % 100 == 0:
                    self.stdout.write(f'Processed {i}/{total} professors...')

                # Get or create departments
                department_names = prof_data.get('Departments', '').split(', ')
                departments = []
                for dept_name in department_names:
                    if dept_name:  # Only process non-empty department names
                        departments.append(dept_name)
                departments = ', '.join(departments)

                # Create professor
                professor = Professor.objects.create(
                    name=prof_data.get('Instructor Name'),
                    departments=departments,
                    total_ratings=prof_data.get('Total Ratings'),
                    empirical_bayes_average=prof_data.get('Empirical Bayes Average'),
                    empirical_bayes_rank=prof_data.get('Empirical Bayes Rank'),
                    overall_letter_grade=prof_data.get('Overall Letter Grade'),
                    intra_department_eb_average=prof_data.get('Intra-Department EB Average'),
                    intra_department_letter_grade=prof_data.get('Intra-Department Letter Grade'),
                    intra_department_ranks=prof_data.get('Intra-Department Ranks')
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully processed {total} professors'))

        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format in professors.json'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
