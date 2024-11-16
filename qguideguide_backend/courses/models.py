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

    def __str__(self):
        return self.title

class FeedbackTable(models.Model):
    course = models.ForeignKey(Course, related_name='feedback_tables', on_delete=models.CASCADE)
    table_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.table_name} for {self.course.title}"

class FeedbackEntry(models.Model):
    feedback_table = models.ForeignKey(FeedbackTable, related_name='entries', on_delete=models.CASCADE)
    raters = models.CharField(max_length=255, blank=True, null=True)
    students = models.CharField(max_length=255, blank=True, null=True)
    statistics = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    options = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    percentage = models.CharField(max_length=50, blank=True, null=True)
    excellent = models.CharField(max_length=50, blank=True, null=True)
    very_good = models.CharField(max_length=50, blank=True, null=True)
    good = models.CharField(max_length=50, blank=True, null=True)
    fair = models.CharField(max_length=50, blank=True, null=True)
    unsatisfactory = models.CharField(max_length=50, blank=True, null=True)
    course_mean = models.FloatField(blank=True, null=True)
    fas_mean = models.FloatField(blank=True, null=True)
    instructor_mean = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Feedback entry for {self.feedback_table.course.title} ({self.feedback_table.table_name})"
