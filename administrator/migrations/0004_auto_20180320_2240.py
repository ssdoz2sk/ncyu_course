# Generated by Django 2.0.2 on 2018-03-20 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0003_coursetemp_teacher_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursetemp',
            name='grade',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
