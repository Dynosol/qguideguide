from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Course(models.Model):
    TERM_CHOICES = [
        ('2019 Fall', '2019 Fall'),
        ('2020 Fall', '2020 Fall'),
        ('2021 Spring', '2021 Spring'),
        ('2021 Fall', '2021 Fall'),
        ('2022 Spring', '2022 Spring'),
        ('2022 Fall', '2022 Fall'),
        ('2023 Spring', '2023 Spring'),
        ('2023 Fall', '2023 Fall'),
    ]

    title = models.CharField(max_length=1000, db_index=True)
    department = models.CharField(max_length=1000, db_index=True)
    instructor = models.CharField(max_length=1000, db_index=True)
    term = models.CharField(max_length=100, choices=TERM_CHOICES, db_index=True)
    subject = models.CharField(max_length=1000)
    blue_course_id = models.CharField(max_length=100)
    url = models.URLField(max_length=1000)
    responses = models.IntegerField(default=0, db_index=True)
    invited_responses = models.IntegerField(default=0)
    response_ratio = models.FloatField(null=True, blank=True)
    course_mean_rating = models.FloatField(null=True, blank=True, db_index=True)
    materials_mean_rating = models.FloatField(null=True, blank=True)
    assignments_mean_rating = models.FloatField(null=True, blank=True)
    feedback_mean_rating = models.FloatField(null=True, blank=True)
    section_mean_rating = models.FloatField(null=True, blank=True)
    instructor_mean_rating = models.FloatField(null=True, blank=True)
    effective_mean_rating = models.FloatField(null=True, blank=True)
    accessible_mean_rating = models.FloatField(null=True, blank=True)
    enthusiasm_mean_rating = models.FloatField(null=True, blank=True)
    discussion_mean_rating = models.FloatField(null=True, blank=True)
    inst_feedback_mean_rating = models.FloatField(null=True, blank=True)
    returns_mean_rating = models.FloatField(null=True, blank=True)
    hours_mean_rating = models.FloatField(null=True, blank=True)
    recommend_mean_rating = models.FloatField(null=True, blank=True)
    number_comments = models.IntegerField(default=0)

    course_mean_rating_bayesian_score = models.FloatField(null=True, blank=True)
    materials_mean_rating_bayesian_score = models.FloatField(null=True, blank=True)
    assignments_mean_rating_bayesian_score = models.FloatField(null=True, blank=True)
    feedback_mean_rating_bayesian_score = models.FloatField(null=True, blank=True)
    section_mean_rating_bayesian_score = models.FloatField(null=True, blank=True)
    instructor_mean_rating_bayesian_score = models.FloatField(null=True, blank=True)
    effective_mean_rating_bayesian_score = models.FloatField(null=True, blank=True)
    accessible_mean_rating_bayesian_score = models.FloatField(null=True, blank=True)
    enthusiasm_mean_rating_bayesian_score = models.FloatField(null=True, blank=True)
    discussion_mean_rating_bayesian_score = models.FloatField(null=True, blank=True)
    inst_feedback_mean_rating_bayesian_score = models.FloatField(null=True, blank=True)
    returns_mean_rating_bayesian_score = models.FloatField(null=True, blank=True)

    course_mean_grade = models.CharField(max_length=2, null=True, blank=True)
    materials_mean_grade = models.CharField(max_length=2, null=True, blank=True)
    assignments_mean_grade = models.CharField(max_length=2, null=True, blank=True)
    feedback_mean_grade = models.CharField(max_length=2, null=True, blank=True)
    section_mean_grade = models.CharField(max_length=2, null=True, blank=True)
    instructor_mean_grade = models.CharField(max_length=2, null=True, blank=True)
    effective_mean_grade = models.CharField(max_length=2, null=True, blank=True)
    accessible_mean_grade = models.CharField(max_length=2, null=True, blank=True)
    enthusiasm_mean_grade = models.CharField(max_length=2, null=True, blank=True)
    discussion_mean_grade = models.CharField(max_length=2, null=True, blank=True)
    inst_feedback_mean_grade = models.CharField(max_length=2, null=True, blank=True)
    returns_mean_grade = models.CharField(max_length=2, null=True, blank=True)

    course_mean_rating_bayesian_score_department = models.FloatField(null=True, blank=True)
    materials_mean_rating_bayesian_score_department = models.FloatField(null=True, blank=True)
    assignments_mean_rating_bayesian_score_department = models.FloatField(null=True, blank=True)
    feedback_mean_rating_bayesian_score_department = models.FloatField(null=True, blank=True)
    section_mean_rating_bayesian_score_department = models.FloatField(null=True, blank=True)
    instructor_mean_rating_bayesian_score_department = models.FloatField(null=True, blank=True)
    effective_mean_rating_bayesian_score_department = models.FloatField(null=True, blank=True)
    accessible_mean_rating_bayesian_score_department = models.FloatField(null=True, blank=True)
    enthusiasm_mean_rating_bayesian_score_department = models.FloatField(null=True, blank=True)
    discussion_mean_rating_bayesian_score_department = models.FloatField(null=True, blank=True)
    inst_feedback_mean_rating_bayesian_score_department = models.FloatField(null=True, blank=True)
    returns_mean_rating_bayesian_score_department = models.FloatField(null=True, blank=True)

    course_mean_grade_department = models.CharField(max_length=2, null=True, blank=True)
    materials_mean_grade_department = models.CharField(max_length=2, null=True, blank=True)
    assignments_mean_grade_department = models.CharField(max_length=2, null=True, blank=True)
    feedback_mean_grade_department = models.CharField(max_length=2, null=True, blank=True)
    section_mean_grade_department = models.CharField(max_length=2, null=True, blank=True)
    instructor_mean_grade_department = models.CharField(max_length=2, null=True, blank=True)
    effective_mean_grade_department = models.CharField(max_length=2, null=True, blank=True)
    accessible_mean_grade_department = models.CharField(max_length=2, null=True, blank=True)
    enthusiasm_mean_grade_department = models.CharField(max_length=2, null=True, blank=True)
    discussion_mean_grade_department = models.CharField(max_length=2, null=True, blank=True)
    inst_feedback_mean_grade_department = models.CharField(max_length=2, null=True, blank=True)
    returns_mean_grade_department = models.CharField(max_length=2, null=True, blank=True)

    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['term', 'department', 'instructor']),
            models.Index(fields=['course_mean_rating', 'department']),
        ]

class CourseFeedbackQuestion(models.Model):
    course = models.ForeignKey(Course, related_name='course_feedback_questions', on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    count = models.IntegerField(default=0)
    excellent_count = models.IntegerField(default=0)
    very_good_count = models.IntegerField(default=0)
    good_count = models.IntegerField(default=0)
    fair_count = models.IntegerField(default=0)
    unsatisfactory_count = models.IntegerField(default=0)
    course_mean = models.FloatField(null=True, blank=True)
    fas_mean = models.FloatField(null=True, blank=True)

class InstructorFeedbackQuestion(models.Model):
    course = models.ForeignKey(Course, related_name='instructor_feedback_questions', on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    count = models.IntegerField(default=0)
    excellent_count = models.IntegerField(default=0)
    very_good_count = models.IntegerField(default=0)
    good_count = models.IntegerField(default=0)
    fair_count = models.IntegerField(default=0)
    unsatisfactory_count = models.IntegerField(default=0)
    fas_mean = models.FloatField(null=True, blank=True)
    instructor_mean = models.FloatField(null=True, blank=True)

class HoursAndRecQuestion(models.Model):
    course = models.OneToOneField(Course, related_name='hours_breakdown', on_delete=models.CASCADE)
    response_count = models.IntegerField(default=0)
    response_ratio = models.FloatField(null=True, blank=True)
    mean = models.FloatField(null=True, blank=True)
    median = models.FloatField(null=True, blank=True)
    mode = models.FloatField(null=True, blank=True)
    standard_dev = models.FloatField(null=True, blank=True)

class CourseComment(models.Model):
    course = models.ForeignKey(Course, related_name='comments', on_delete=models.CASCADE)
    comment_text = models.TextField()