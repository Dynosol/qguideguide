import json
import os
from urllib import response
from django.core.management.base import BaseCommand
from django.db import transaction
from pandas import ExcelFile
from courses.models import Course, CourseFeedbackQuestion, InstructorFeedbackQuestion, HoursAndRecQuestion, CourseComment

class Command(BaseCommand):
    help = 'Import course data from JSON file'

    # THERE"S SOMETHING BAD WITH THE ROUNDING HERE!!!!! ## REMMEBER ####
    def get_counts_from_percentages(self, percentages, total_count):
        total_count = int(total_count)
        counts = []
        
        # First pass: calculate counts based on rounded percentages
        for percent in percentages:
            if percent in ["NRP", "NA", "", "N/A", "0%", "N/"]:
                counts.append(0)
                continue
            count = round((self.clean_float_value(percent[:-1]) / 100) * total_count)
            counts.append(count)

        return counts

    def clean_float_value(self, string_input):
        if string_input == "0%":
            return float(0)
        if not string_input or string_input in ["NRP", "NA", "", "N/A"]:
            return None
        if "%" in string_input:
            return float(string_input[:-1]) / 100
        try:
            return float(string_input)
        except ValueError:
            self.stdout.write(self.style.ERROR(f"Unable to convert to float: {string_input}"))
            return None

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'static', 'json', 'course_data.json')

        self.stdout.write(self.style.SUCCESS(f'Reading data from {file_path}'))

        with open(file_path, 'r') as f:
            course_data_list = json.load(f)

        self.stdout.write(self.style.SUCCESS(f'Found {len(course_data_list)} courses to import'))

        courses_created = 0
        feedback_created = 0
        comments_created = 0

        for course_data in course_data_list:
            # Log course being processed
            self.stdout.write(f'Processing course: {course_data.get("Title")}')

            try:
                with transaction.atomic():
                    if Course.objects.filter(title=course_data.get('Title'), instructor=course_data.get('Instructor'), term=course_data.get('Term')).exists():
                        self.stdout.write(self.style.WARNING(f"Course '{course_data.get('Title')}' by '{course_data.get('Instructor')}' for term '{course_data.get('Term')}' already exists. Skipping."))
                        continue

                    # is default value of zero bad?? we'll worry about that later
                    def safe_get(lst, index, default=None): # the data is SO NASTYYYYY
                        try:
                            return lst[index]
                        except IndexError:
                            return default if default is not None else {}

                    feedback_data = course_data.get('Feedback', {})
                    if len(feedback_data) > 0:
                        responses = int(feedback_data.get("course_response_rate", [{}])[0].get("Students", 0))
                        invited_responses = int(feedback_data.get("course_response_rate", [{}])[1].get("Students", 0))
                        response_ratio = self.clean_float_value(safe_get(feedback_data.get("course_response_rate", [{}]), 2, {}).get("Students", 0.0))

                        course_mean_rating = self.clean_float_value(safe_get(feedback_data.get("course_general_questions", [{}]), 0, {}).get("Course Mean", None))
                        materials_mean_rating = self.clean_float_value(safe_get(feedback_data.get("course_general_questions", [{}]), 1, {}).get("Course Mean", None))
                        assignments_mean_rating = self.clean_float_value(safe_get(feedback_data.get("course_general_questions", [{}]), 2, {}).get("Course Mean", None))
                        feedback_mean_rating = self.clean_float_value(safe_get(feedback_data.get("course_general_questions", [{}]), 3, {}).get("Course Mean", None))
                        section_mean_rating = self.clean_float_value(safe_get(feedback_data.get("course_general_questions", [{}]), 4, {}).get("Course Mean", None))

                        instructor_mean_rating = self.clean_float_value(safe_get(feedback_data.get("general_instructor_questions", [{}]), 0, {}).get("Instructor Mean", None))
                        effective_mean_rating = self.clean_float_value(safe_get(feedback_data.get("general_instructor_questions", [{}]), 1, {}).get("Instructor Mean", None))
                        accessible_mean_rating = self.clean_float_value(safe_get(feedback_data.get("general_instructor_questions", [{}]), 2, {}).get("Instructor Mean", None))
                        enthusiasm_mean_rating = self.clean_float_value(safe_get(feedback_data.get("general_instructor_questions", [{}]), 3, {}).get("Instructor Mean", None))
                        discussion_mean_rating = self.clean_float_value(safe_get(feedback_data.get("general_instructor_questions", [{}]), 4, {}).get("Instructor Mean", None))
                        inst_feedback_mean_rating = self.clean_float_value(safe_get(feedback_data.get("general_instructor_questions", [{}]), 5, {}).get("Instructor Mean", None))
                        returns_mean_rating = self.clean_float_value(safe_get(feedback_data.get("general_instructor_questions", [{}]), 6, {}).get("Instructor Mean", None))

                        hours_mean_rating = self.clean_float_value(safe_get(feedback_data.get("on_average,_how_many_hours_per_week_did_you_spend_on_coursework_outside_of_class?_enter_a_whole_number_between_0_and_168.", [{}]), 2, {}).get("Value", 0))
                        recommend_mean_rating = self.clean_float_value(safe_get(feedback_data.get("how_strongly_would_you_recommend_this_course_to_your_peers?", [{}]), 1, {}).get("Value", None))
                        number_comments = len(feedback_data.get("comments_from_students", []))

                        instructor = feedback_data.get('Instructor Name', [{}])[0].get('Instructor Name', course_data.get('Instructor'))
                    else:
                        responses = 0
                        invited_responses = 0
                        response_ratio = 0.0
                        course_mean_rating = None
                        materials_mean_rating = None
                        assignments_mean_rating = None
                        feedback_mean_rating = None
                        section_mean_rating = None
                        instructor_mean_rating = None
                        effective_mean_rating = None
                        accessible_mean_rating = None
                        enthusiasm_mean_rating = None
                        discussion_mean_rating = None
                        inst_feedback_mean_rating = None
                        returns_mean_rating = None
                        hours_mean_rating = 0
                        recommend_mean_rating = None
                        number_comments = 0
                        
                        instructor=course_data.get('Instructor'),

                    # Create course explicitly
                    course = Course.objects.create(
                        title=course_data.get('Title'),
                        department=course_data.get('Department'),
                        instructor=instructor,
                        term=course_data.get('Term'),
                        subject=course_data.get('Subject'),
                        blue_course_id=course_data.get('Bluecourseid'),
                        url=course_data.get('Url'),
                        responses = responses,
                        invited_responses = invited_responses,
                        response_ratio = response_ratio,
                        course_mean_rating = course_mean_rating,
                        materials_mean_rating = materials_mean_rating,
                        assignments_mean_rating = assignments_mean_rating,
                        feedback_mean_rating = feedback_mean_rating,
                        section_mean_rating = section_mean_rating,
                        instructor_mean_rating = instructor_mean_rating,
                        effective_mean_rating = effective_mean_rating,
                        accessible_mean_rating = accessible_mean_rating,
                        enthusiasm_mean_rating = enthusiasm_mean_rating,
                        discussion_mean_rating = discussion_mean_rating,
                        inst_feedback_mean_rating = inst_feedback_mean_rating,
                        returns_mean_rating = returns_mean_rating,
                        hours_mean_rating = hours_mean_rating,
                        recommend_mean_rating = recommend_mean_rating,
                        number_comments = number_comments,
                    )
                    courses_created += 1

                    # Handle feedback questions
                    course_feedback_data = course_data.get('Feedback', {}).get('course_general_questions', [])
                    for question_data in course_feedback_data:
                        rating_counts = self.get_counts_from_percentages([question_data.get('Excellent'), question_data.get('Very Good'), question_data.get('Good'), question_data.get('Fair'), question_data.get('Unsatisfactory')], question_data.get('Count'))
                        CourseFeedbackQuestion.objects.create(
                            course=course,
                            question=question_data.get(''),
                            count=question_data.get('Count'),
                            excellent_count=rating_counts[0],
                            very_good_count=rating_counts[1],
                            good_count=rating_counts[2],
                            fair_count=rating_counts[3],
                            unsatisfactory_count=rating_counts[4],
                            course_mean=self.clean_float_value(question_data.get('Course Mean')),
                            fas_mean=self.clean_float_value(question_data.get('FAS Mean'))
                        )

                    feedback_created += 1

                    instructor_feedback_data = course_data.get('Feedback', {}).get('general_instructor_questions', [])
                    for question_data in instructor_feedback_data:
                        rating_counts = self.get_counts_from_percentages([question_data.get('Excellent'), question_data.get('Very Good'), question_data.get('Good'), question_data.get('Fair'), question_data.get('Unsatisfactory')], question_data.get('Count'))
                        InstructorFeedbackQuestion.objects.create(
                            course=course,
                            question=question_data.get(''),
                            count=question_data.get('Count'),
                            excellent_count=rating_counts[0],
                            very_good_count=rating_counts[1],
                            good_count=rating_counts[2],
                            fair_count=rating_counts[3],
                            unsatisfactory_count=rating_counts[4],
                            instructor_mean=self.clean_float_value(question_data.get('Instructor Mean')),
                            fas_mean=self.clean_float_value(question_data.get('FAS Mean'))
                        )

                    feedback_created += 1


                    hours_data = course_data.get('Feedback', {}).get('hours_and_rec_questions', [])
                    for question_data in hours_data:
                        HoursAndRecQuestion.objects.create(
                            course=course,
                            response_count=self.clean_numeric_value(question_data.get('Response Count')) or 0,
                            response_ratio=self.clean_float_value(question_data.get('Response Ratio')),
                            mean=self.clean_float_value(question_data.get('Mean')),
                            median=self.clean_float_value(question_data.get('Median')),
                            mode=self.clean_float_value(question_data.get('Mode')),
                            standard_dev=self.clean_float_value(question_data.get('Standard Deviation'))
                        )

                    # Handle comments
                    comments_data = course_data.get('Feedback', {}).get('comments_from_students', [])
                    for comment in comments_data:
                        if comment.get('Comments'):
                            CourseComment.objects.create(
                                course=course,
                                comment_text=comment['Comments']
                            )
                    comments_created += 1

            except Exception as e:
                # Print out all the details of the course that failed
                self.stdout.write(self.style.ERROR(f'''
                Error: {e}
                '''))
                continue

            if courses_created % 10 == 0:
                self.stdout.write(f'Processed {courses_created} courses...')

        self.stdout.write(self.style.SUCCESS(f'''
Import completed successfully:
- Courses created: {courses_created}
- Feedback questions created: {feedback_created}
- Comments created: {comments_created}
'''))
