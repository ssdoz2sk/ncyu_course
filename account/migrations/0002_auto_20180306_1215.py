# Generated by Django 2.0.2 on 2018-03-06 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseuser',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='courseuser',
            name='department',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='courseuser',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
