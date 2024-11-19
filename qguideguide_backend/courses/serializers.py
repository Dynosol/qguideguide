# courses/serializers.py
from rest_framework import serializers
from .models import Course, Instructor

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ('id', 'name')

class CourseSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer()  # Nested serializer if needed

    class Meta:
        model = Course
        fields = ('id', 'title', 'department', 'instructor', 'term', 'students_enrolled', 'response_count', 'response_rate')
