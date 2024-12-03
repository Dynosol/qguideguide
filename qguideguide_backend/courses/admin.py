from django.contrib import admin
from .models import Course, CourseRatingBreakdown, CourseComment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'department', 'term', 'overall_score', 'response_rate')
    list_filter = ('department', 'term')
    search_fields = ('title', 'instructor', 'department', 'blue_course_id')
    ordering = ('-term', 'department', 'title')

@admin.register(CourseRatingBreakdown)
class CourseRatingBreakdownAdmin(admin.ModelAdmin):
    list_display = ('course', 'excellent_count', 'very_good_count', 'good_count', 'fair_count', 'unsatisfactory_count', 'course_mean')
    search_fields = ('course__title',)
    list_filter = ('course__department',)

@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ('course', 'comment_text')
    search_fields = ('course__title', 'comment_text')
    list_filter = ('course__department',)
