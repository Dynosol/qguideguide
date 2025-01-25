# courses/serializers.py
from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    """Serializer for course model"""
    class Meta:
        model = Course
        fields = '__all__'