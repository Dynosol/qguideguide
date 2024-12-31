import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import QuerySet
from courses.models import Course

class Command(BaseCommand):
    help = "Add Empirical Bayes (normal prior) scores + percentile-based letter grades to existing Course objects"

    # Map your model fields to the corresponding question keys in the JSON:
    QUESTION_MAP = {
        "course_mean_rating":        "Evaluate the course overall.",
        "materials_mean_rating":     "Course materials (readings, audio-visual materials, textbooks, lab manuals, website, etc.)",
        "assignments_mean_rating":   "Assignments (exams, essays, problem sets, language homework, etc.)",
        "feedback_mean_rating":      "Feedback you received on work you produced in this course",
        "section_mean_rating":       "Section component of the course",
        "instructor_mean_rating":    "Evaluate your Instructor overall.",
        "effective_mean_rating":     "Gives effective lectures or presentations, if applicable",
        "accessible_mean_rating":    "Is accessible outside of class (including after class, office hours, e-mail, etc.)",
        "enthusiasm_mean_rating":    "Generates enthusiasm for the subject matter",
        "discussion_mean_rating":    "Facilitates discussion and encourages participation",
        "inst_feedback_mean_rating": "Gives useful feedback on assignments",
        "returns_mean_rating":       "Returns assignments in a timely fashion",
    }

    grade_boundaries = [ # NOTE THAT THIS IS PERCENTILES, NOT RAW, SO GRADING IS UNCONVENTIONAL
        (0, 0.1, 'S+'),
        (0.1, 0.5, 'S'),
        (0.5, 1, 'S-'),
        (1, 2, 'A+'),
        (2, 5, 'A'),
        (5, 10, 'A-'),
        (10, 20, 'B+'),
        (20, 40, 'B'),
        (40, 60, 'B-'),
        (60, 80, 'C'),
        (80, 95, 'D'),
        (95, 100, 'F'),
    ]

    def assign_letter_grade(self, percentile: float) -> str:
        """
        Convert the given percentile rank (0-100) to a letter grade
        using the boundaries in grade_boundaries. The percentile is
        first reversed (0 -> 100, 100 -> 0) before comparing.
        """

        for lower, upper, grade in self.grade_boundaries:
            if lower <= percentile < upper:
                return grade

        # Fallback letter grade if no match
        return 'F'

    def handle(self, *args, **kwargs):
        """
        Main entry point for the management command. Loads JSON data, validates it,
        calculates Empirical Bayes (EB) scores, then saves updated Course objects
        with EB scores and percentile-based letter grades.
        """
        self.stdout.write(
            self.style.SUCCESS("Starting Empirical Bayes + Percentile Grade update...")
        )

        # 1) Load the JSON data
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )
        file_path = os.path.join(base_dir, 'static', 'json', 'import_summary.json')
        self.stdout.write(self.style.SUCCESS(f"Reading data from {file_path}"))

        try:
            with open(file_path, 'r') as f:
                import_summary = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Error decoding JSON: {e}"))
            return

        # 2) Validate the JSON structure to ensure we have the necessary keys
        for key in ("Counts", "Sums", "SumOfSquares"):
            if key not in import_summary:
                self.stdout.write(
                    self.style.ERROR(f"JSON missing global '{key}'. Cannot proceed.")
                )
                return

        for key in ("Counts by Department", "Sums by Department", "SumOfSquares by Department"):
            if key not in import_summary:
                self.stdout.write(
                    self.style.ERROR(f"JSON missing '{key}'. Cannot proceed.")
                )
                return

        # 3) Define helper functions

        def get_global_stats(question: str):
            """
            Return (mean, variance) across ALL departments/courses for the given question.
            If no data is found, returns (None, None).
            """
            total_count = import_summary["Counts"].get(question, 0)
            total_sum = import_summary["Sums"].get(question, 0.0)
            total_sum_squares = import_summary["SumOfSquares"].get(question, 0.0)

            if total_count <= 0:
                return None, None

            mean_ = total_sum / total_count
            e_x2 = total_sum_squares / total_count  # E(X^2)
            var_ = max(e_x2 - (mean_ ** 2), 0.0)
            return mean_, var_

        def get_department_stats(question: str, department: str):
            """
            Return (mean, variance) for the given question in the specified department.
            If no data is found, returns (None, None).
            """
            dept_counts = import_summary["Counts by Department"].get(department, {})
            dept_sums = import_summary["Sums by Department"].get(department, {})
            dept_sum_squares = import_summary["SumOfSquares by Department"].get(department, {})

            dept_count = dept_counts.get(question, 0)
            sum_ = dept_sums.get(question, 0.0)
            sum_sq_ = dept_sum_squares.get(question, 0.0)

            if dept_count <= 0:
                return None, None

            mean_ = sum_ / dept_count
            e_x2 = sum_sq_ / dept_count
            var_ = max(e_x2 - (mean_ ** 2), 0.0)
            return mean_, var_

        def calculate_eb_normal(observed_mean, n_responses, prior_mean, prior_variance):
            """
            Calculate Normal-Prior Empirical Bayes score for a single observation.
            If we can't compute a prior or have no data (n_responses=0), returns None.
            """
            if prior_mean is None or prior_variance is None:
                return None

            if n_responses <= 0:
                return None

            # Observed variance for a mean is 1 / n
            observed_variance = 1.0 / n_responses

            # Weight controlling how much to 'shrink' the observed_mean
            shrinkage_weight = prior_variance / (prior_variance + observed_variance)

            # EB estimate is a blend of prior_mean and observed_mean
            eb_score = shrinkage_weight * observed_mean + (1 - shrinkage_weight) * prior_mean
            return eb_score

        # 4) Collect EB scores in memory for percentile calculation.
        #    For each field in QUESTION_MAP, we store:
        #    eb_global[field] -> list of (course_id, global_eb)
        #    eb_dept[field]   -> list of (course_id, dept_eb)
        eb_global = {field: [] for field in self.QUESTION_MAP}
        eb_dept = {field: [] for field in self.QUESTION_MAP}

        # Keep a quick-access map from course ID to the Course instance
        course_map = {}
        courses_updated = 0

        # 5) Main transaction
        try:
            with transaction.atomic():
                # Retrieve all Course objects
                all_courses: QuerySet[Course] = Course.objects.all()

                # First Pass: Compute EB scores and store them in memory
                for course in all_courses:
                    course_map[course.id] = course
                    department_name = course.department or "Unknown"

                    # Compute EB for each rating field
                    for field_name, question_key in self.QUESTION_MAP.items():
                        observed_mean = getattr(course, field_name, None)
                        n_responses = getattr(course, 'responses', 0)

                        # Skip if there's no rating data for this field
                        if observed_mean is None or n_responses <= 0:
                            continue

                        # 1) Global EB
                        g_mean, g_var = get_global_stats(question_key)
                        global_eb = calculate_eb_normal(
                            observed_mean=observed_mean,
                            n_responses=n_responses,
                            prior_mean=g_mean,
                            prior_variance=g_var
                        )
                        setattr(course, f"{field_name}_bayesian_score", round(global_eb, 2))
                        eb_global[field_name].append((course.id, global_eb))

                        # 2) Department EB
                        d_mean, d_var = get_department_stats(question_key, department_name)
                        dept_eb = calculate_eb_normal(
                            observed_mean=observed_mean,
                            n_responses=n_responses,
                            prior_mean=d_mean,
                            prior_variance=d_var
                        )
                        setattr(course, f"{field_name}_bayesian_score_department", round(dept_eb, 2))
                        eb_dept[field_name].append((course.id, dept_eb))

                # Second Pass: Compute percentile ranks and letter grades (global & dept)
                for field_name in self.QUESTION_MAP:
                    # 2A: Global EB percentile ranking
                    all_data_global = eb_global[field_name]
                    if not all_data_global:
                        continue

                    # Sort descending by EB score
                    sorted_global = sorted(all_data_global, key=lambda x: x[1], reverse=True)
                    total_global = len(sorted_global)

                    # Assign letter grades by percentile
                    for rank, (course_id, score) in enumerate(sorted_global, start=1):
                        percentile = (rank / total_global) * 100.0
                        grade = self.assign_letter_grade(percentile)

                        # Build the grade field name
                        base_name = field_name.replace("_mean_rating", "")
                        grade_field_name = f"{base_name}_mean_grade"

                        # Set the global letter grade on the Course object
                        course_map[course_id].__dict__[grade_field_name] = grade

                    # 2B: Department EB percentile ranking
                    all_data_dept = eb_dept[field_name]
                    if not all_data_dept:
                        continue

                    # Sort descending by EB score
                    sorted_dept = sorted(all_data_dept, key=lambda x: x[1], reverse=True)
                    total_dept = len(sorted_dept)

                    # Assign department-level letter grades by percentile
                    for rank, (course_id, score) in enumerate(sorted_dept, start=1):
                        percentile = (rank / total_dept) * 100.0
                        dept_grade = self.assign_letter_grade(percentile)

                        base_name = field_name.replace("_mean_rating", "")
                        dept_grade_field_name = f"{base_name}_mean_grade_department"
                        course_map[course_id].__dict__[dept_grade_field_name] = dept_grade

                # Third Pass: Save all updated Course objects
                for course_id, course_obj in course_map.items():
                    course_obj.save()
                    courses_updated += 1

                    # Periodic progress message
                    if courses_updated % 10 == 0:
                        self.stdout.write(f"{courses_updated} courses updated...")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during update: {e}"))

        # Done
        self.stdout.write(
            self.style.SUCCESS(
                f"Empirical Bayes + Percentile Grade update completed. "
                f"Courses updated: {courses_updated}"
            )
        )