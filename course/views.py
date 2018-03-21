from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from comment.forms import CommentForm
from comment.models import Comment
from course.forms import SearchForm
from course.models import Course


def course_search(request):
    form = SearchForm(request.GET)

    if form.is_valid():
        data = form.cleaned_data
        if not data['course_name']:
            return render(request, 'course/course_list.html', {'search_form': form})

        courses = Course.objects.filter(name__icontains=data['course_name']).distinct('course_num', 'teacher_name')
        return render(request, 'course/course_list.html', {'search_form': form, 'courses': courses})

    return render(request, 'course/course_list.html', {'search_form': form})


def course_detail(request, course_num):
    courses = Course.objects.filter(course_num=course_num).distinct('teacher_name')
    if len(courses) == 0:
        raise Http404("Course does not exist")

    course = courses[0]
    teachers = [c.teacher_name for c in courses]

    comment_form = CommentForm()

    comments = Comment.objects.filter(course_num=course_num)

    return render(request, 'course/course_detail.html', {
        'course': course, 'teachers': teachers, 'form': comment_form, 'comments': comments})

