from django import template

register = template.Library()


@register.inclusion_tag('course/tag/course_star.html')
def star():
    pass
