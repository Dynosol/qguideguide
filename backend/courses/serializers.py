# courses/serializers.py
from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id',
                  'title',
                  'department',
                  'instructor',
                  'term',
                  'invited_responses',
                  'course_mean_rating',
                  'hours_mean_rating',
                  'instructor_mean_rating',
                  'url')
