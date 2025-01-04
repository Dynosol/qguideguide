# models.py

from django.db import models
from django.db.models import Avg


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    empirical_bayes_average = models.FloatField(null=True, blank=True)
    empirical_bayes_rank = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Professor(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    departments = models.CharField(max_length=100, null=True, blank=True)
    total_ratings = models.FloatField(null=True, blank=True)
    empirical_bayes_average = models.FloatField(null=True, blank=True)
    empirical_bayes_rank = models.IntegerField(null=True, blank=True)
    overall_letter_grade = models.CharField(max_length=2, null=True, blank=True)
    intra_department_eb_average = models.FloatField(null=True, blank=True)
    intra_department_letter_grade = models.CharField(max_length=2, null=True, blank=True)
    intra_department_ranks = models.CharField(max_length=255, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


