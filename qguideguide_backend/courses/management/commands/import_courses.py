import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from courses.models import Course, Instructor, CourseRatingBreakdown, CourseComment
from django.db.models import Count

class Command(BaseCommand):
    help = 'Import course data from JSON file'

    def clean_numeric_value(self, value):
        if value in ['NRP', '', None]:
            return None
        try:
            # Handle percentage strings
            if isinstance(value, str) and '%' in value:
                value = value.replace('%', '')
            return int(float(value))  # Convert to int for count fields
        except (ValueError, TypeError):
            return None

    def clean_percentage(self, value):
        if not value:
            return None
        try:
            # Remove % sign and convert to float
            return float(value.replace('%', ''))
        except (ValueError, TypeError, AttributeError):
            return None

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'static', 'json', 'course_data.json')
        
        self.stdout.write(self.style.SUCCESS(f'Reading data from {file_path}'))
        
        with open(file_path, 'r') as f:
            course_data_list = json.load(f)

        self.stdout.write(self.style.SUCCESS(f'Found {len(course_data_list)} courses to import'))

        with transaction.atomic():
            courses_created = 0
            ratings_created = 0
            comments_created = 0

            for course_data in course_data_list:
                # Print course name when processing it
                self.stdout.write(f'Processing course: {course_data.get("Title")}')

                # Create or get instructor
                instructor_name = course_data.get('Instructor')
                instructor, _ = Instructor.objects.get_or_create(name=instructor_name)

                # Create or update course
                course, created = Course.objects.update_or_create(
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
                        'response_rate': self.clean_percentage(course_data.get('Response Rate %')),
                    }
                )

                if created:
                    courses_created += 1

                # Process feedback data
                feedback_data = course_data.get('Feedback', {})
                
                # Table_2 typically contains the overall course ratings
                if 'Table_2' in feedback_data and feedback_data['Table_2']:
                    table_2 = feedback_data['Table_2'][0]  # Get first entry
                    
                    defaults = {
                        'excellent_count': self.clean_numeric_value(table_2.get('Excellent')) or 0,
                        'very_good_count': self.clean_numeric_value(table_2.get('Very Good')) or 0,
                        'good_count': self.clean_numeric_value(table_2.get('Good')) or 0,
                        'fair_count': self.clean_numeric_value(table_2.get('Fair')) or 0,
                        'unsatisfactory_count': self.clean_numeric_value(table_2.get('Unsatisfactory')) or 0,
                        'course_mean': self.clean_numeric_value(table_2.get('Course Mean')),
                        'fas_mean': self.clean_numeric_value(table_2.get('FAS Mean')),
                        'instructor_mean': self.clean_numeric_value(table_2.get('Instructor Mean')),
                    }
                    
                    rating_breakdown, created = CourseRatingBreakdown.objects.update_or_create(
                        course=course,
                        defaults=defaults
                    )
                    
                    if created:
                        ratings_created += 1

                    # Update course overall score from Table_2
                    course.overall_score = self.clean_numeric_value(table_2.get('Course Mean'))
                    course.save()

                # Process comments if they exist (usually in Table_3)
                if 'Table_3' in feedback_data:
                    for entry in feedback_data['Table_3']:
                        if 'Value' in entry and entry['Value']:
                            comment, created = CourseComment.objects.get_or_create(
                                course=course,
                                comment_text=entry['Value']
                            )
                            if created:
                                comments_created += 1

                if courses_created % 10 == 0:
                    self.stdout.write(f'Processed {courses_created} courses...')

        # Update instructor departments based on most common department
        for instructor in Instructor.objects.all():
            primary_dept = instructor.primary_department()
            if primary_dept:
                instructor.department = primary_dept
                instructor.save()

        self.stdout.write(self.style.SUCCESS(f'''
Import completed successfully:
- Courses created/updated: {courses_created}
- Rating breakdowns created: {ratings_created}
- Comments created: {comments_created}
'''))
