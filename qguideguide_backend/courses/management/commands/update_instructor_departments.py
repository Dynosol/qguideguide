from django.core.management.base import BaseCommand
from courses.models import Instructor

class Command(BaseCommand):
    help = 'Updates instructor departments based on their most common course department'

    def handle(self, *args, **kwargs):
        for instructor in Instructor.objects.all():
            primary_dept = instructor.primary_department()
            if primary_dept:
                instructor.department = primary_dept
                instructor.save()
                self.stdout.write(f'Updated {instructor.name} with department: {primary_dept}') 