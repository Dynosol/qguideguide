# Generated by Django 5.1.3 on 2024-12-06 04:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('department', models.CharField(max_length=255)),
                ('instructor', models.CharField(max_length=255)),
                ('term', models.CharField(choices=[('2019 Fall', '2019 Fall'), ('2020 Fall', '2020 Fall'), ('2021 Spring', '2021 Spring'), ('2021 Fall', '2021 Fall'), ('2022 Spring', '2022 Spring'), ('2022 Fall', '2022 Fall'), ('2023 Spring', '2023 Spring'), ('2023 Fall', '2023 Fall')], max_length=100)),
                ('subject', models.CharField(max_length=255)),
                ('blue_course_id', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('responses', models.IntegerField(default=0)),
                ('invited_responses', models.IntegerField(default=0)),
                ('response_ratio', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('course_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('materials_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('assignments_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('feedback_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('section_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('instructor_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('effective_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('accessible_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('enthusiasm_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('discussion_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('inst_feedback_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('returns_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('hours_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('recommend_mean_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('number_comments', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CourseComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseFeedbackQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('count', models.IntegerField(default=0)),
                ('excellent_count', models.IntegerField(default=0)),
                ('very_good_count', models.IntegerField(default=0)),
                ('good_count', models.IntegerField(default=0)),
                ('fair_count', models.IntegerField(default=0)),
                ('unsatisfactory_count', models.IntegerField(default=0)),
                ('course_mean', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('fas_mean', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_feedback_questions', to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='HoursAndRecQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_count', models.IntegerField(default=0)),
                ('response_ratio', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('mean', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('median', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('mode', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('standard_dev', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hours_breakdown', to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='InstructorFeedbackQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('count', models.IntegerField(default=0)),
                ('excellent_count', models.IntegerField(default=0)),
                ('very_good_count', models.IntegerField(default=0)),
                ('good_count', models.IntegerField(default=0)),
                ('fair_count', models.IntegerField(default=0)),
                ('unsatisfactory_count', models.IntegerField(default=0)),
                ('fas_mean', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('instructor_mean', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructor_feedback_questions', to='courses.course')),
            ],
        ),
    ]
