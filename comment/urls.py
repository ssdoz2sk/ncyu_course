from django.urls import path
from django.views.generic import RedirectView
from .views import post_comment

urlpatterns = [
    path('<slug:course_num>/', post_comment, name='post_comment'),
]