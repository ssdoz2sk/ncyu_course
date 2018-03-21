from django.db import models

# Create your models here.
from django.utils import timezone
from course.models import Course


class Comment(models.Model):
    course_num = models.CharField(max_length=20, blank=True, null=True)
    reply = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, default="匿名")
    email = models.CharField(max_length=200, blank=True)
    teacher_name = models.CharField(max_length=20)

    hidden = models.BooleanField()

    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return self.text