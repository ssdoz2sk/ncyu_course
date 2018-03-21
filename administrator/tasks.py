from __future__ import absolute_import, unicode_literals
from celery import shared_task

from .units.curriculum import get_course_async


def curriculum(year, semester):
    task_id = get_course_async(year, semester)
    return task_id



