# Generated by Django 5.1.3 on 2025-01-25 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professors', '0012_department_professor_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
