from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail

from django.conf import settings

@shared_task()
def task_send_confirm_email(email, subject, message):
    if isinstance(email, str):
        email = [email]

    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, email, fail_silently=False, html_message=message)

    return mail_sent
