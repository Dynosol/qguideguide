from django.contrib import admin
from .models import Course, CourseFeedbackQuestion, InstructorFeedbackQuestion, HoursAndRecQuestion, CourseComment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
    'title', 'department', 'instructor', 'term', 'subject',
    'responses', 'invited_responses', 'response_ratio',
    'course_mean_rating', 'materials_mean_rating', 'assignments_mean_rating',
    'feedback_mean_rating', 'section_mean_rating', 'instructor_mean_rating',
    'effective_mean_rating', 'accessible_mean_rating', 'enthusiasm_mean_rating',
    'discussion_mean_rating', 'inst_feedback_mean_rating', 'returns_mean_rating',
    'hours_mean_rating', 'recommend_mean_rating', 'number_comments',
    'course_mean_rating_bayesian_score', 'materials_mean_rating_bayesian_score',
    'assignments_mean_rating_bayesian_score', 'feedback_mean_rating_bayesian_score',
    'section_mean_rating_bayesian_score', 'instructor_mean_rating_bayesian_score',
    'effective_mean_rating_bayesian_score', 'accessible_mean_rating_bayesian_score',
    'enthusiasm_mean_rating_bayesian_score', 'discussion_mean_rating_bayesian_score',
    'inst_feedback_mean_rating_bayesian_score', 'returns_mean_rating_bayesian_score',
    'course_mean_rating_bayesian_score_department', 'materials_mean_rating_bayesian_score_department',
    'assignments_mean_rating_bayesian_score_department', 'feedback_mean_rating_bayesian_score_department',
    'section_mean_rating_bayesian_score_department', 'instructor_mean_rating_bayesian_score_department',
    'effective_mean_rating_bayesian_score_department', 'accessible_mean_rating_bayesian_score_department',
    'enthusiasm_mean_rating_bayesian_score_department', 'discussion_mean_rating_bayesian_score_department',
    'inst_feedback_mean_rating_bayesian_score_department', 'returns_mean_rating_bayesian_score_department',
    'course_mean_grade', 'materials_mean_grade', 'assignments_mean_grade',
    'feedback_mean_grade', 'section_mean_grade', 'instructor_mean_grade',
    'effective_mean_grade', 'accessible_mean_grade', 'enthusiasm_mean_grade',
    'discussion_mean_grade', 'inst_feedback_mean_grade', 'returns_mean_grade',
    'course_mean_grade_department', 'materials_mean_grade_department',
    'assignments_mean_grade_department', 'feedback_mean_grade_department',
    'section_mean_grade_department', 'instructor_mean_grade_department',
    'effective_mean_grade_department', 'accessible_mean_grade_department',
    'enthusiasm_mean_grade_department', 'discussion_mean_grade_department',
    'inst_feedback_mean_grade_department', 'returns_mean_grade_department'
    )
    list_filter = ('term', 'department', 'instructor')
    search_fields = ('title', 'instructor', 'department', 'subject')
    readonly_fields = (
        'responses', 'invited_responses', 'response_ratio',
        'course_mean_rating', 'materials_mean_rating', 'assignments_mean_rating',
        'feedback_mean_rating', 'section_mean_rating', 'instructor_mean_rating',
        'effective_mean_rating', 'accessible_mean_rating', 'enthusiasm_mean_rating',
        'discussion_mean_rating', 'inst_feedback_mean_rating', 'returns_mean_rating',
        'hours_mean_rating', 'recommend_mean_rating', 'number_comments',
        'course_mean_rating_bayesian_score', 'materials_mean_rating_bayesian_score',
        'assignments_mean_rating_bayesian_score', 'feedback_mean_rating_bayesian_score',
        'section_mean_rating_bayesian_score', 'instructor_mean_rating_bayesian_score',
        'effective_mean_rating_bayesian_score', 'accessible_mean_rating_bayesian_score',
        'enthusiasm_mean_rating_bayesian_score', 'discussion_mean_rating_bayesian_score',
        'inst_feedback_mean_rating_bayesian_score', 'returns_mean_rating_bayesian_score',
        'course_mean_rating_bayesian_score_department', 'materials_mean_rating_bayesian_score_department',
        'assignments_mean_rating_bayesian_score_department', 'feedback_mean_rating_bayesian_score_department',
        'section_mean_rating_bayesian_score_department', 'instructor_mean_rating_bayesian_score_department',
        'effective_mean_rating_bayesian_score_department', 'accessible_mean_rating_bayesian_score_department',
        'enthusiasm_mean_rating_bayesian_score_department', 'discussion_mean_rating_bayesian_score_department',
        'inst_feedback_mean_rating_bayesian_score_department', 'returns_mean_rating_bayesian_score_department',
        'course_mean_grade', 'materials_mean_grade', 'assignments_mean_grade',
        'feedback_mean_grade', 'section_mean_grade', 'instructor_mean_grade',
        'effective_mean_grade', 'accessible_mean_grade', 'enthusiasm_mean_grade',
        'discussion_mean_grade', 'inst_feedback_mean_grade', 'returns_mean_grade',
        'course_mean_grade_department', 'materials_mean_grade_department',
        'assignments_mean_grade_department', 'feedback_mean_grade_department',
        'section_mean_grade_department', 'instructor_mean_grade_department',
        'effective_mean_grade_department', 'accessible_mean_grade_department',
        'enthusiasm_mean_grade_department', 'discussion_mean_grade_department',
        'inst_feedback_mean_grade_department', 'returns_mean_grade_department'
    )
    
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'department', 'instructor', 'term', 'subject', 'blue_course_id', 'url')
        }),
        ('Response Information', {
            'fields': ('responses', 'invited_responses', 'response_ratio')
        }),
        ('Mean Ratings', {
            'fields': (
                'course_mean_rating', 'materials_mean_rating', 'assignments_mean_rating',
                'feedback_mean_rating', 'section_mean_rating', 'instructor_mean_rating',
                'effective_mean_rating', 'accessible_mean_rating', 'enthusiasm_mean_rating',
                'discussion_mean_rating', 'inst_feedback_mean_rating', 'returns_mean_rating',
                'hours_mean_rating', 'recommend_mean_rating'
            )
        }),
        ('Empirical Bayes Scores', {
            'fields': (
                'course_mean_rating_bayesian_score', 'materials_mean_rating_bayesian_score',
                'assignments_mean_rating_bayesian_score', 'feedback_mean_rating_bayesian_score',
                'section_mean_rating_bayesian_score', 'instructor_mean_rating_bayesian_score',
                'effective_mean_rating_bayesian_score', 'accessible_mean_rating_bayesian_score',
                'enthusiasm_mean_rating_bayesian_score', 'discussion_mean_rating_bayesian_score',
                'inst_feedback_mean_rating_bayesian_score', 'returns_mean_rating_bayesian_score'
            )
        }),
        ('Department-Level Empirical Bayes Scores', {
            'fields': (
                'course_mean_rating_bayesian_score_department', 'materials_mean_rating_bayesian_score_department',
                'assignments_mean_rating_bayesian_score_department', 'feedback_mean_rating_bayesian_score_department',
                'section_mean_rating_bayesian_score_department', 'instructor_mean_rating_bayesian_score_department',
                'effective_mean_rating_bayesian_score_department', 'accessible_mean_rating_bayesian_score_department',
                'enthusiasm_mean_rating_bayesian_score_department', 'discussion_mean_rating_bayesian_score_department',
                'inst_feedback_mean_rating_bayesian_score_department', 'returns_mean_rating_bayesian_score_department'
            )
        }),
        ('Mean Grades', {
            'fields': (
                'course_mean_grade', 'materials_mean_grade', 'assignments_mean_grade',
                'feedback_mean_grade', 'section_mean_grade', 'instructor_mean_grade',
                'effective_mean_grade', 'accessible_mean_grade', 'enthusiasm_mean_grade',
                'discussion_mean_grade', 'inst_feedback_mean_grade', 'returns_mean_grade'
            )
        }),
        ('Department-Level Mean Grades', {
            'fields': (
                'course_mean_grade_department', 'materials_mean_grade_department',
                'assignments_mean_grade_department', 'feedback_mean_grade_department',
                'section_mean_grade_department', 'instructor_mean_grade_department',
                'effective_mean_grade_department', 'accessible_mean_grade_department',
                'enthusiasm_mean_grade_department', 'discussion_mean_grade_department',
                'inst_feedback_mean_grade_department', 'returns_mean_grade_department'
            )
        }),
        ('Other Information', {
            'fields': ('number_comments',)
        }),
    )

@admin.register(CourseFeedbackQuestion)
class CourseFeedbackQuestion(admin.ModelAdmin):
    list_display = ('course', 'question', 'excellent_count', 'very_good_count', 'good_count', 'fair_count', 'unsatisfactory_count', 'course_mean', 'fas_mean')
    list_filter = ('course',)
    search_fields = ('course__title', 'question')
    
    fieldsets = (
        ('Feedback Details', {
            'fields': ('course', 'question', 'excellent_count', 'very_good_count', 'good_count', 'fair_count', 'unsatisfactory_count')
        }),
        ('Mean Ratings', {
            'fields': ('course_mean', 'fas_mean')
        }),
    )

@admin.register(InstructorFeedbackQuestion)
class InstructorFeedbackQuestion(admin.ModelAdmin):
    list_display = ('course', 'question', 'excellent_count', 'very_good_count', 'good_count', 'fair_count', 'unsatisfactory_count', 'instructor_mean', 'fas_mean')
    list_filter = ('course',)
    search_fields = ('course__title', 'question')
    
    fieldsets = (
        ('Feedback Details', {
            'fields': ('course', 'question', 'excellent_count', 'very_good_count', 'good_count', 'fair_count', 'unsatisfactory_count')
        }),
        ('Mean Ratings', {
            'fields': ('course_mean', 'fas_mean')
        }),
    )

@admin.register(HoursAndRecQuestion)
class HoursAndRecQuestionAdmin(admin.ModelAdmin):
    list_display = ('course', 'response_count', 'response_ratio', 'mean', 'median', 'mode', 'standard_dev')
    list_filter = ('course',)
    search_fields = ('course__title',)
    
    fieldsets = (
        ('Hours and Recommendation Details', {
            'fields': ('course', 'response_count', 'response_ratio', 'mean', 'median', 'mode', 'standard_dev')
        }),
    )

@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ('course', 'comment_text')
    list_filter = ('course',)
    search_fields = ('course__title', 'comment_text')
    
    fieldsets = (
        ('Comment Details', {
            'fields': ('course', 'comment_text')
        }),
    )
