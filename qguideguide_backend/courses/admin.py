from django.contrib import admin
from .models import Course, CourseFeedbackQuestion, InstructorFeedbackQuestion, HoursAndRecQuestion, CourseComment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'department', 'instructor', 'term', 'subject', 'responses', 
        'invited_responses', 'response_ratio', 'course_mean_rating', 
        'instructor_mean_rating', 'recommend_mean_rating', 'number_comments'
    )
    list_filter = ('term', 'department', 'instructor')
    search_fields = ('title', 'instructor', 'department', 'subject')
    readonly_fields = (
        'course_mean_rating', 'materials_mean_rating', 'assignments_mean_rating',
        'feedback_mean_rating', 'section_mean_rating', 'instructor_mean_rating',
        'effective_mean_rating', 'accessible_mean_rating', 'enthusiasm_mean_rating',
        'discussion_mean_rating', 'inst_feedback_mean_rating', 'returns_mean_rating',
        'hours_mean_rating', 'recommend_mean_rating', 'number_comments'
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
