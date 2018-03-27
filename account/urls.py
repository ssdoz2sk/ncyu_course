from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from account import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='profile', permanent=False)),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^account$', views.account, name='account'),
    path(r'email_confirmation', views.email_confirmation, name='email_confirmation'),
]