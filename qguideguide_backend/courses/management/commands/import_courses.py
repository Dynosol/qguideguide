import json
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import course data from JSON file'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'static', 'course_data.json')
        with open(file_path, 'r') as f:
            course_data_list = json.load(f)

        for course_data in course_data_list:
            instructor_name = course_data.get('Instructor')
            title = course_data.get('Title')
            department = course_data.get('Department')
            term = course_data.get('Term')
            subject = course_data.get('Subject')
            blue_course_id = course_data.get('Bluecourseid')
            url = course_data.get('Url')

            print(f"Course Title: {title}")
            print(f"Instructor: {instructor_name}")
            print(f"Department: {department}")
            print(f"Term: {term}")
            print(f"Subject: {subject}")
            print(f"Blue Course ID: {blue_course_id}")
            print(f"URL: {url}")
            print("-------------------------------------------")

        self.stdout.write(self.style.SUCCESS('Successfully printed course data'))
