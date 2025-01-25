from rest_framework import serializers
from .models import Professor, Department

class DepartmentSerializer(serializers.ModelSerializer):
    professor_count = serializers.IntegerField(required=False)
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'empirical_bayes_average', 'empirical_bayes_rank', 'professor_count']

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'
