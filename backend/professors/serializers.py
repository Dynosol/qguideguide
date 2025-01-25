from rest_framework import serializers
from .models import Professor, Department
from django.core.exceptions import FieldDoesNotExist

class DepartmentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically remove fields that don't exist in the model
        model_fields = [f.name for f in Department._meta.get_fields()]
        for field_name in list(self.fields.keys()):
            if field_name not in model_fields:
                self.fields.pop(field_name)
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'empirical_bayes_average', 'empirical_bayes_rank', 'professor_count']

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'
