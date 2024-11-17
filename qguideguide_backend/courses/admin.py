# so I can see the course dbs in the django admin interface
from django.contrib import admin
from .models import Course, Instructor, CourseRatingBreakdown, CourseComment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'department', 'term', 'response_rate', 'overall_score')
    list_filter = ('department', 'term', 'instructor')
    search_fields = ('title', 'instructor__name', 'department')

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'department')

@admin.register(CourseRatingBreakdown)
class CourseRatingBreakdownAdmin(admin.ModelAdmin):
    list_display = ('course', 'course_mean', 'fas_mean', 'instructor_mean')
    search_fields = ('course__title', 'course__instructor__name')

@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ('course', 'comment_text')
    search_fields = ('course__title', 'comment_text')
