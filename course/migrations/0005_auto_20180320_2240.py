# Generated by Django 2.0.2 on 2018-03-20 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_course_teacher_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='grade',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
