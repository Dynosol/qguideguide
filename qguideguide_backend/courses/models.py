from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    TERM_CHOICES = [
        ('2019 Fall', '2019 Fall'), # must be "actual value, human-readable value tuples for some reason...??"
        ('2020 Fall', '2020 Fall'),
        ('2021 Spring', '2021 Spring'),
        ('2021 Fall', '2021 Fall'),
        ('2022 Spring', '2022 Spring'),
        ('2022 Fall', '2022 Fall'),
        ('2023 Spring', '2023 Spring'),
        ('2023 Fall', '2023 Fall'),
    ]

    title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)  # Changed from ForeignKey to CharField
    term = models.CharField(max_length=100, choices=TERM_CHOICES)
    subject = models.CharField(max_length=255)
    blue_course_id = models.CharField(max_length=100)
    url = models.URLField()

    students_enrolled = models.IntegerField(null=True, blank=True, default=0)
    response_count = models.IntegerField(null=True, blank=True, default=0)
    response_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0)

    overall_score = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    workload_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    difficulty_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    would_recommend_percent = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, default=0
    )

    class Meta:
        ordering = ['-term', 'department', 'title']
        indexes = [
            models.Index(fields=['department']),
            models.Index(fields=['term']),
            models.Index(fields=['overall_score']),
        ]

    def __str__(self):
        return f"{self.title} - {self.instructor} ({self.term})"


class CourseRatingBreakdown(models.Model):
    course = models.OneToOneField(Course, related_name='rating_breakdown', on_delete=models.CASCADE)

    excellent_count = models.IntegerField(default=0)  # Default to 0
    very_good_count = models.IntegerField(default=0)  # Default to 0
    good_count = models.IntegerField(default=0)  # Default to 0
    fair_count = models.IntegerField(default=0)  # Default to 0
    unsatisfactory_count = models.IntegerField(default=0)  # Default to 0

    course_mean = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    fas_mean = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    instructor_mean = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Rating Breakdown for {self.course.title}"


class CourseComment(models.Model):
    course = models.ForeignKey(Course, related_name='comments', on_delete=models.CASCADE)
    comment_text = models.TextField()

    def __str__(self):
        return f"Comment for {self.course.title}: {self.comment_text[:50]}..."
