# courses/serializers.py
from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    """Serializer for course model"""
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'department', 'instructor', 'term', 
            'subject', 'responses', 'course_mean_rating',
            'materials_mean_rating', 'assignments_mean_rating',
            'feedback_mean_rating', 'section_mean_rating',
            'instructor_mean_rating'
        ]