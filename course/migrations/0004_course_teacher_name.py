# Generated by Django 2.0.2 on 2018-03-20 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_course_schooltime'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]