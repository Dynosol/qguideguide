# Generated by Django 5.1.3 on 2025-01-04 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professors', '0004_remove_professor_department_professor_departments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='empirical_bayes_rank',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
