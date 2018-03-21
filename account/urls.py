from django.conf.urls import url
from django.views.generic import RedirectView

from account import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='profile', permanent=False)),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^account$', views.account, name='account'),
]