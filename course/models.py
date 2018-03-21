from django.db import models
from django.contrib.postgres.fields import HStoreField, JSONField


# Create your models here.
from django.urls import reverse


class Course(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    credit = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    semester = models.IntegerField(default=0)
    course_num = models.CharField(max_length=20, blank=True, null=True)
    course_type = models.CharField(max_length=50, blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=20, blank=True, null=True)
    college = models.CharField(max_length=20, blank=True, null=True)
    schooltime = JSONField(default=[])
    teacher_name = models.TextField(blank=True,null=True)
    student_limit = models.IntegerField(default=0)
    student_select = models.IntegerField(default=0)


    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'course_num': self.course_num})