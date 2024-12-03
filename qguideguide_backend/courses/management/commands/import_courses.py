import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from courses.models import Course, CourseRatingBreakdown, CourseComment


class Command(BaseCommand):
    help = 'Import course data from JSON file'

    def clean_numeric_value(self, value):
        if value in ['NRP', '', None]:
            return None
        try:
            if isinstance(value, str) and '%' in value:
                value = value.replace('%', '')
            return int(float(value))
        except (ValueError, TypeError):
            return None

    def clean_percentage(self, value):
        if not value:
            return None
        try:
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
                # Log course being processed
                self.stdout.write(f'Processing course: {course_data.get("Title")}')

                # Create course explicitly
                course = Course.objects.create(
                    title=course_data.get('Title'),
                    department=course_data.get('Department'),
                    instructor=course_data.get('Instructor'),
                    term=course_data.get('Term'),
                    subject=course_data.get('Subject'),
                    blue_course_id=course_data.get('Bluecourseid'),
                    url=course_data.get('Url'),
                    students_enrolled=course_data.get('Students Enrolled'),
                    response_count=course_data.get('Student Response Count'),
                    response_rate=self.clean_percentage(course_data.get('Response Rate %')),
                    overall_score=self.clean_numeric_value(
                        course_data.get('Feedback', {}).get('course_general_questions', [{}])[0].get('Course Mean')
                    ),
                )
                courses_created += 1

                # Handle course general questions
                feedback_data = course_data.get('Feedback', {})
                if 'course_general_questions' in feedback_data and feedback_data['course_general_questions']:
                    course_general_questions = feedback_data['course_general_questions'][0]
                    
                    CourseRatingBreakdown.objects.create(
                        course=course,
                        excellent_count=self.clean_numeric_value(course_general_questions.get('Excellent')) or 0,
                        very_good_count=self.clean_numeric_value(course_general_questions.get('Very Good')) or 0,
                        good_count=self.clean_numeric_value(course_general_questions.get('Good')) or 0,
                        fair_count=self.clean_numeric_value(course_general_questions.get('Fair')) or 0,
                        unsatisfactory_count=self.clean_numeric_value(course_general_questions.get('Unsatisfactory')) or 0,
                        course_mean=self.clean_numeric_value(course_general_questions.get('Course Mean')),
                        fas_mean=self.clean_numeric_value(course_general_questions.get('FAS Mean')),
                        instructor_mean=self.clean_numeric_value(course_general_questions.get('Instructor Mean')),
                    )
                    ratings_created += 1

                # Handle comments
                if 'comments_from_students' in feedback_data:
                    for entry in feedback_data['comments_from_students']:
                        if 'Comments' in entry and entry['Comments']:
                            CourseComment.objects.create(
                                course=course,
                                comment_text=entry['Comments']
                            )
                            comments_created += 1

                if courses_created % 10 == 0:
                    self.stdout.write(f'Processed {courses_created} courses...')

        self.stdout.write(self.style.SUCCESS(f'''
Import completed successfully:
- Courses created: {courses_created}
- Rating breakdowns created: {ratings_created}
- Comments created: {comments_created}
'''))
