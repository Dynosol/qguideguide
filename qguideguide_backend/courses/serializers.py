# courses/serializers.py
from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'department', 'instructor', 'term', 'students_enrolled', 'response_count', 'response_rate')
