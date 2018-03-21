from django.db import models

# Create your models here.
from account.models import CourseUser
from course.models import Course


class Teacher(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

    courses = models.ManyToManyField(Course, related_name="teachers")
    user = models.ForeignKey(CourseUser)


