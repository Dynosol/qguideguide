from collections import defaultdict
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
        
    def find_item_by_question_contains(self, data_list, question_key, substring):
        """
        Searches for a dictionary in data_list where data_dict[question_key] contains the substring.
        
        :param data_list: List of dictionaries to search through.
        :param question_key: The key in the dictionary that holds the question text.
        :param substring: The substring to match within the question text.
        :return: The matching dictionary or None if not found.
        """
        for item in data_list:
            question_text = item.get(question_key, "")
            if substring in question_text:
                return item
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

        # for calculating bayesian scores
        counts = defaultdict(int)
        sums = defaultdict(float)

        global_sum_of_squares_dict = defaultdict(float)
        dept_sum_of_squares_dict = defaultdict(lambda: defaultdict(float))

        counts_by_department = defaultdict(lambda: defaultdict(int))
        sums_by_department = defaultdict(lambda: defaultdict(float))

        for course_data in course_data_list:
            # Log course being processed
            self.stdout.write(f'Processing course: {course_data.get("Title")}')

            try:
                with transaction.atomic():
                    if Course.objects.filter(url=course_data.get('Url')).exists(): # for some reason other checks didn't work as well..
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

                        course_general_questions = feedback_data.get("course_general_questions", [])
                        evaluate_course = self.find_item_by_question_contains(course_general_questions, "", "Evaluate the course overall.")
                        course_mean_rating = self.clean_float_value(evaluate_course.get("Course Mean")) if evaluate_course else None
                        evaluate_materials = self.find_item_by_question_contains(course_general_questions, "", "Course materials (readings, audio-visual materials, textbooks, lab manuals, website, etc.)")
                        materials_mean_rating = self.clean_float_value(evaluate_materials.get("Course Mean")) if evaluate_materials else None
                        evaluate_assignments = self.find_item_by_question_contains(course_general_questions, "", "Assignments (exams, essays, problem sets, language homework, etc.)")
                        assignments_mean_rating = self.clean_float_value(evaluate_assignments.get("Course Mean")) if evaluate_assignments else None
                        evaluate_feedback = self.find_item_by_question_contains(course_general_questions, "", "Feedback you received on work you produced in this course")
                        feedback_mean_rating = self.clean_float_value(evaluate_feedback.get("Course Mean")) if evaluate_feedback else None
                        evaluate_section = self.find_item_by_question_contains(course_general_questions, "", "Section component of the course")
                        section_mean_rating = self.clean_float_value(evaluate_section.get("Course Mean")) if evaluate_section else None

                        general_instructor_questions = feedback_data.get("general_instructor_questions", [])
                        evaluate_instructor = self.find_item_by_question_contains(general_instructor_questions, "", "Evaluate your Instructor overall.")
                        instructor_mean_rating = self.clean_float_value(evaluate_instructor.get("Instructor Mean")) if evaluate_instructor else None
                        evaluate_effectiveness = self.find_item_by_question_contains(general_instructor_questions, "", "Gives effective lectures or presentations, if applicable")
                        effective_mean_rating = self.clean_float_value(evaluate_effectiveness.get("Instructor Mean")) if evaluate_effectiveness else None
                        evaluate_accessibility = self.find_item_by_question_contains(general_instructor_questions, "", "Is accessible outside of class (including after class, office hours, e-mail, etc.)")
                        accessible_mean_rating = self.clean_float_value(evaluate_accessibility.get("Instructor Mean")) if evaluate_accessibility else None
                        evaluate_enthusiasm = self.find_item_by_question_contains(general_instructor_questions, "", "Generates enthusiasm for the subject matter")
                        enthusiasm_mean_rating = self.clean_float_value(evaluate_enthusiasm.get("Instructor Mean")) if evaluate_enthusiasm else None
                        evaluate_discussion = self.find_item_by_question_contains(general_instructor_questions, "", "Facilitates discussion and encourages participation")
                        discussion_mean_rating = self.clean_float_value(evaluate_discussion.get("Instructor Mean")) if evaluate_discussion else None
                        evaluate_feedback = self.find_item_by_question_contains(general_instructor_questions, "", "Gives useful feedback on assignments")
                        inst_feedback_mean_rating = self.clean_float_value(evaluate_feedback.get("Instructor Mean")) if evaluate_feedback else None
                        evaluate_returns = self.find_item_by_question_contains(general_instructor_questions, "", "Returns assignments in a timely fashion")
                        returns_mean_rating = self.clean_float_value(evaluate_returns.get("Instructor Mean")) if evaluate_returns else None

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
                        
                        instructor=course_data.get('Instructor')

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
                    #
                    # These are lowkey depricated, but we'll keep them for now
                    # 
                    course_feedback_data = course_data.get('Feedback', {}).get('course_general_questions', [])
                    for question_data in course_feedback_data:
                        rating_counts = self.get_counts_from_percentages([question_data.get('Excellent'), question_data.get('Very Good'), question_data.get('Good'), question_data.get('Fair'), question_data.get('Unsatisfactory')], question_data.get('Count'))
                        question = question_data.get('') 
                        if "If this course was conducted in a lecture format with the involvement of section leaders, one or more of the following questions may not be applicable." in question: # will likely have to change later
                            question = "Facilitates discussion and encourages participation"
                        CourseFeedbackQuestion.objects.create(
                            course=course,
                            question=question,
                            count=question_data.get('Count'),
                            excellent_count=rating_counts[0],
                            very_good_count=rating_counts[1],
                            good_count=rating_counts[2],
                            fair_count=rating_counts[3],
                            unsatisfactory_count=rating_counts[4],
                            course_mean=self.clean_float_value(question_data.get('Course Mean')),
                            fas_mean=self.clean_float_value(question_data.get('FAS Mean'))
                        )
                        counts[question] += 1
                        sums_add = self.clean_float_value(question_data.get('Course Mean'))
                        if sums_add is not None:
                            sums[question] += sums_add
                            global_sum_of_squares_dict[question] += sums_add ** 2
                        counts_by_department[course_data.get('Department')][question] += 1
                        sums_dep_add = self.clean_float_value(question_data.get('Course Mean'))
                        if sums_dep_add is not None:
                            sums_by_department[course_data.get('Department')][question] += sums_dep_add
                            dept_sum_of_squares_dict[course_data.get('Department')][question] += sums_dep_add ** 2

                        feedback_created += 1


                    #
                    # This is also depricated, but we'll keep it for now
                    #
                    instructor_feedback_data = course_data.get('Feedback', {}).get('general_instructor_questions', [])
                    for question_data in instructor_feedback_data:
                        rating_counts = self.get_counts_from_percentages([question_data.get('Excellent'), question_data.get('Very Good'), question_data.get('Good'), question_data.get('Fair'), question_data.get('Unsatisfactory')], question_data.get('Count'))
                        question = question_data.get('') 
                        if "If this course was conducted in a lecture format with the involvement of section leaders, one or more of the following questions may not be applicable." in question: # will likely have to change later
                            question = "Facilitates discussion and encourages participation"
                        InstructorFeedbackQuestion.objects.create(
                            course=course,
                            question=question,
                            count=question_data.get('Count'),
                            excellent_count=rating_counts[0],
                            very_good_count=rating_counts[1],
                            good_count=rating_counts[2],
                            fair_count=rating_counts[3],
                            unsatisfactory_count=rating_counts[4],
                            instructor_mean=self.clean_float_value(question_data.get('Instructor Mean')),
                            fas_mean=self.clean_float_value(question_data.get('FAS Mean'))
                        )
                        counts[question] += 1
                        sums_add = self.clean_float_value(question_data.get('Instructor Mean'))
                        if sums_add is not None:
                            sums[question] += sums_add
                            global_sum_of_squares_dict[question] += sums_add ** 2
                        counts_by_department[course_data.get('Department')][question] += 1
                        sums_dep_add = self.clean_float_value(question_data.get('Instructor Mean'))
                        if sums_dep_add is not None:
                            sums_by_department[course_data.get('Department')][question] += sums_dep_add
                            dept_sum_of_squares_dict[course_data.get('Department')][question] += sums_dep_add ** 2

                        feedback_created += 1

                    #
                    # this too, is depricated, but we'll keep it for now
                    #
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

        self.stdout.write(
            self.style.SUCCESS(f'''
            Import completed successfully:
            - Courses created: {courses_created}
            - Feedback questions created: {feedback_created}
            - Comments created: {comments_created}
            ''')
        )






        # ================================================================================================
        #
        # FOR BAYESIAN CALCULATIONS
        #
        # ================================================================================================
        counts_dict = dict(counts)
        sums_dict = dict(sums)
        counts_by_department_dict = {dept: dict(questions) for dept, questions in counts_by_department.items()}
        sums_by_department_dict = {dept: dict(questions) for dept, questions in sums_by_department.items()}

        # Consolidate all data into a single dictionary
        summary_data = {
            "Import Summary": {
                "Courses Created": courses_created,
                "Feedback Questions Created": feedback_created,
                "Comments Created": comments_created
            },
            "Counts": counts_dict,
            "Sums": sums_dict,
            "SumOfSquares": global_sum_of_squares_dict,
            "Counts by Department": counts_by_department_dict,
            "SumOfSquares by Department": dept_sum_of_squares_dict,
            "Sums by Department": sums_by_department_dict
        }

        # Define the output JSON file path
        output_json_path = os.path.join(base_dir, 'static', 'json', 'import_summary.json')

        # Write the summary data to the JSON file
        try:
            with open(output_json_path, 'w') as json_file:
                json.dump(summary_data, json_file, indent=4)
            self.stdout.write(self.style.SUCCESS(f'Summary data successfully written to {output_json_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to write summary data to JSON: {e}'))