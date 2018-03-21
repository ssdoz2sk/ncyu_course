from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from comment.forms import CommentForm
from course.models import Course


def post_comment(request, course_num, reply_pk=None):
    courses = Course.objects.filter(course_num=course_num)

    if len(courses) == 0:
        raise Http404("Course does not exist")

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            comment.hidden = False

            comment.course_num = course_num

            comment.save()

            return redirect(courses[0])

    return redirect(courses[0])