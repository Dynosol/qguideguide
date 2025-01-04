import json
import os
from collections import defaultdict
from django.core.management.base import BaseCommand
from django.conf import settings
from professors.models import Department

class Command(BaseCommand):
    help = 'Process departments from professors.json and calculate department-wide statistics'

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

            # Department statistics tracking
            dept_stats = defaultdict(lambda: {
                'count': 0,
                'eb_sum': 0,
                'rank_sum': 0
            })

            # Read and process the JSON file
            with open(file_path, 'r') as file:
                professors_data = json.load(file)

            # Process each professor
            for prof in professors_data:
                # Some professors might have multiple departments
                departments = prof['Departments'].split(', ')
                
                for dept in departments:
                    dept_stats[dept]['count'] += 1
                    dept_stats[dept]['eb_sum'] += prof['Empirical Bayes Average']
                    dept_stats[dept]['rank_sum'] += prof['Empirical Bayes Rank']

            # Instead of deleting all departments, we'll update or create them
            total_depts = len(dept_stats)
            self.stdout.write(f'Processing {total_depts} departments...')

            for dept_name, stats in dept_stats.items():
                count = stats['count']
                eb_avg = stats['eb_sum'] / count
                rank_avg = stats['rank_sum'] / count
                print(dept_name, eb_avg, rank_avg)

                Department.objects.update_or_create(
                    name=dept_name,  # This is the lookup field
                    defaults={       # These fields will be updated if the department exists
                        'empirical_bayes_average': eb_avg,
                        'empirical_bayes_rank': rank_avg
                    }
                )

                print(f"Department {dept_name} updated with EB Average: {eb_avg}, Rank Average: {rank_avg}")

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully processed {total_depts} departments'
                )
            )

        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR('Invalid JSON format in professors.json')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'An error occurred: {str(e)}')
            )
