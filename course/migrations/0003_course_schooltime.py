# Generated by Django 2.0.2 on 2018-03-20 07:36

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20180320_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='schooltime',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[]),
        ),
    ]
