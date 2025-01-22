import json
import os
from collections import defaultdict
from django.core.management.base import BaseCommand
from django.conf import settings
from professors.models import Department
import re

class Command(BaseCommand):
    help = 'Process departments from professors.json and calculate department-wide statistics'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to professors.json file')

    def parse_department_metrics(self, metrics_str):
        if not metrics_str:
            return []
        
        departments = []
        pattern = re.compile(r'([A-Za-z-]+):\s([\d.]+)\s\(.*Rank:\s(\d+)')
        parts = metrics_str.split('|')
        
        for part in parts:
            part = part.strip()
            match = pattern.match(part)
            if match:
                dept_name = match.group(1)
                dept_avg = float(match.group(2))
                dept_rank = int(match.group(3))
                departments.append((dept_name, dept_avg, dept_rank))
        
        return departments

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
                'eb_sum': 0.0,
                'rank_sum': 0
            })

            # Read and process the JSON file
            with open(file_path, 'r') as file:
                professors_data = json.load(file)

            # Process each professor
            for prof in professors_data:
                dept_metrics = self.parse_department_metrics(prof.get('Department Metrics'))

                for dept_name, dept_avg, dept_rank in dept_metrics:
                    dept_stats[dept_name]['count'] += 1
                    dept_stats[dept_name]['eb_sum'] += dept_avg
                    dept_stats[dept_name]['rank_sum'] += dept_rank

            total_depts = len(dept_stats)
            self.stdout.write(f'Processing {total_depts} departments...')

            # Update or create Department records
            for dept_name, stats in dept_stats.items():
                count = stats['count']
                if count > 0:
                    eb_avg = stats['eb_sum'] / count
                    rank_avg = stats['rank_sum'] / count

                    Department.objects.update_or_create(
                        name=dept_name,
                        defaults={
                            'empirical_bayes_average': eb_avg,
                            'empirical_bayes_rank': rank_avg
                        }
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully processed {total_depts} departments'
                )
            )

        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format in professors.json'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))