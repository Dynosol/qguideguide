### NOTE!!!! the json was moved into ./static/json, and isn't just in /static now. change that when you run this again.

import json
import os
from django.core.management.base import BaseCommand
from courses.models import Course, Instructor, FeedbackTable, FeedbackEntry
from django.db import transaction

class Command(BaseCommand):
    help = 'Import course data from JSON file'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'static', 'course_data.json')
        
        self.stdout.write(self.style.SUCCESS(f'Reading data from {file_path}'))
        
        with open(file_path, 'r') as f:
            course_data_list = json.load(f)

        self.stdout.write(self.style.SUCCESS(f'Found {len(course_data_list)} courses to import'))

        with transaction.atomic():
            courses_created = 0
            feedback_tables_created = 0
            feedback_entries_created = 0

            def clean_numeric_value(value):
                if value in ['NRP', '', None]:
                    return None
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return None

            for course_data in course_data_list:
                # Create or get instructor
                instructor_name = course_data.get('Instructor')
                instructor, created = Instructor.objects.get_or_create(name=instructor_name)
                if created:
                    self.stdout.write(f'Created new instructor: {instructor_name}')

                # Create course
                course, created = Course.objects.get_or_create(
                    blue_course_id=course_data.get('Bluecourseid'),
                    defaults={
                        'title': course_data.get('Title'),
                        'department': course_data.get('Department'),
                        'instructor': instructor,
                        'term': course_data.get('Term'),
                        'subject': course_data.get('Subject'),
                        'url': course_data.get('Url'),
                        'students_enrolled': course_data.get('Students Enrolled'),
                        'response_count': course_data.get('Student Response Count'),
                        'response_rate': course_data.get('Response Rate %')
                    }
                )
                if created:
                    courses_created += 1
                    self.stdout.write(f'Created course: {course.title}')
                else:
                    self.stdout.write(f'Found existing course: {course.title}')

                # Process feedback tables
                feedback_data = course_data.get('Feedback', {})
                for table_name, entries in feedback_data.items():
                    feedback_table = FeedbackTable.objects.create(
                        course=course,
                        table_name=table_name,
                        question_text=entries[0].get('Question Text') if entries else None
                    )
                    feedback_tables_created += 1

                    # Create feedback entries
                    for entry in entries:
                        FeedbackEntry.objects.create(
                            feedback_table=feedback_table,
                            raters=entry.get('Raters'),
                            students=entry.get('Students'),
                            statistics=entry.get('Statistics'),
                            value=entry.get('Value'),
                            options=entry.get('Options'),
                            count=entry.get('Count'),
                            percentage=entry.get('Percentage'),
                            excellent=clean_numeric_value(entry.get('Excellent')),
                            very_good=clean_numeric_value(entry.get('Very Good')),
                            good=clean_numeric_value(entry.get('Good')),
                            fair=clean_numeric_value(entry.get('Fair')),
                            unsatisfactory=clean_numeric_value(entry.get('Unsatisfactory')),
                            course_mean=clean_numeric_value(entry.get('Course Mean')),
                            fas_mean=clean_numeric_value(entry.get('FAS Mean')),
                            instructor_mean=clean_numeric_value(entry.get('Instructor Mean'))
                        )
                        feedback_entries_created += 1

                if courses_created % 10 == 0:
                    self.stdout.write(f'Processed {courses_created} courses...')

        self.stdout.write(self.style.SUCCESS(f'''
Import completed successfully:
- Courses created: {courses_created}
- Feedback tables created: {feedback_tables_created}
- Feedback entries created: {feedback_entries_created}
'''))