from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from course.views import course_search, course_detail

urlpatterns = [
    path(r'', RedirectView.as_view(pattern_name='course_search', permanent=False)),
    path(r'search/', course_search, name='course_search'),
    path('<slug:course_num>/', course_detail, name='course_detail'),
]