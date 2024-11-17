from django.db import models

class Instructor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    instructor = models.ForeignKey(Instructor, related_name='courses', on_delete=models.CASCADE)
    term = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    blue_course_id = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    students_enrolled = models.IntegerField(null=True, blank=True)
    response_count = models.IntegerField(null=True, blank=True)
    response_rate = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.instructor.name}"

class FeedbackTable(models.Model):
    course = models.ForeignKey(Course, related_name='feedback_tables', on_delete=models.CASCADE)
    table_name = models.CharField(max_length=50)
    question_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.table_name} for {self.course.title}"

class FeedbackEntry(models.Model):
    feedback_table = models.ForeignKey(FeedbackTable, related_name='entries', on_delete=models.CASCADE)
    raters = models.CharField(max_length=255, null=True, blank=True)
    students = models.CharField(max_length=255, null=True, blank=True)
    statistics = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    options = models.CharField(max_length=255, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    percentage = models.CharField(max_length=50, null=True, blank=True)
    excellent = models.CharField(max_length=50, null=True, blank=True)
    very_good = models.CharField(max_length=50, null=True, blank=True)
    good = models.CharField(max_length=50, null=True, blank=True)
    fair = models.CharField(max_length=50, null=True, blank=True)
    unsatisfactory = models.CharField(max_length=50, null=True, blank=True)
    course_mean = models.FloatField(null=True, blank=True)
    fas_mean = models.FloatField(null=True, blank=True)
    instructor_mean = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Entry for {self.feedback_table.course.title}"