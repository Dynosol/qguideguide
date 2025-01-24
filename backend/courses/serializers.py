# courses/serializers.py
from rest_framework import serializers
from .models import Course

class CourseListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for course list view"""
    class Meta:
        model = Course
        fields = ('id', 'title', 'department', 'instructor', 'term', 
                 'course_mean_rating', 'responses')

class CourseSerializer(serializers.ModelSerializer):
    """Full serializer for course detail view"""
    class Meta:
        model = Course
        fields = '__all__'