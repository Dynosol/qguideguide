# Generated by Django 5.1.3 on 2025-01-04 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professors', '0005_alter_professor_empirical_bayes_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='empirical_bayes_rank',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
