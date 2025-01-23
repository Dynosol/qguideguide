import json
import os
from collections import defaultdict
from django.core.management.base import BaseCommand
from django.conf import settings
from professors.models import Department

class Command(BaseCommand):
    help = 'Calculate department statistics from professor data'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to professors.json file')

    def handle(self, *args, **options):
        try:
            # Get file path from arguments or use default
            file_path = options.get('file') or os.path.join(
                settings.BASE_DIR, 'professors/static/json/professors.json'
            )

            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
                return

            # Initialize department statistics
            department_stats = defaultdict(lambda: {
                'eb_scores': [],
                'global_ranks': [],
                'professor_count': 0
            })

            # Process JSON data
            with open(file_path, 'r') as f:
                professors = json.load(f)

            for prof in professors:
                # Get departments from comma-separated string
                departments = [d.strip() for d in prof['Departments'].split(',') if d.strip()]
                
                # Skip professors without department info
                if not departments:
                    continue
                
                # Get numerical values
                try:
                    eb_score = float(prof['EB Score'])
                    global_rank = int(prof['Global Rank'])
                except (ValueError, KeyError):
                    continue
                
                # Update department stats
                for dept in departments:
                    department_stats[dept]['eb_scores'].append(eb_score)
                    department_stats[dept]['global_ranks'].append(global_rank)
                    department_stats[dept]['professor_count'] += 1

            # Calculate final department metrics
            for dept_name, stats in department_stats.items():
                # Calculate averages
                avg_eb = sum(stats['eb_scores']) / len(stats['eb_scores']) if stats['eb_scores'] else 0
                avg_rank = sum(stats['global_ranks']) / len(stats['global_ranks']) if stats['global_ranks'] else 0
                
                # Update or create department record
                Department.objects.update_or_create(
                    name=dept_name,
                    defaults={
                        'empirical_bayes_average': round(avg_eb, 2),
                        'empirical_bayes_rank': round(avg_rank, 2),
                        'professor_count': stats['professor_count']
                    }
                )

            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated {len(department_stats)} departments')
            )

        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format in professors.json'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing departments: {str(e)}'))