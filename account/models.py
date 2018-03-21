from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.urls import reverse


class CourseUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)

    is_ban = models.BooleanField(default=False)

    ban_type = models.IntegerField(default=0)
    ban_until = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        if self.pk:
            return reverse('user_detail', kwargs={'pk': self.pk})
        else:
            return reverse('user_list')
