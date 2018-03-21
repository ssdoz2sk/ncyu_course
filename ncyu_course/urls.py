"""ncyu_course URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.urls import include
from django.urls import path

from base.views import landingPage
from account import views as account_views

urlpatterns = [
    path('django_admin/', admin.site.urls),

    path('social-auth/', include('social_django.urls', namespace='social')),

    path('settings/', include('account.urls')),
    path('courses/', include('course.urls')),
    path('comments/', include('comment.urls')),

    path('login/', login, {'template_name': 'account/login.html'}, name='login'),
    path('logout/', logout, {'template_name': 'account/logout.html'}, name='logout'),
    path('register/', account_views.register, name="register"),
    path('',  landingPage, name='landingPage' )
]
