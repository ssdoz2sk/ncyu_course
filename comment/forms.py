from django import forms
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from comment.models import Comment


class CommentForm(forms.ModelForm):
    # captcha = ReCaptchaField(widget=ReCaptchaWidget(size='normal'))

    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']