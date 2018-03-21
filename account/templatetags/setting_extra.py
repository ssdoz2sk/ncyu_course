from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag()
def is_active(request, *url_names):
    for urlname in url_names:
        if reverse(urlname) in request.path:
            return 'active'
    return ''

