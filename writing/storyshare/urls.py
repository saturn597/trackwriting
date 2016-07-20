from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'storyshare'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url('^login$',
        auth_views.login,
        { 'template_name': 'storyshare/login.html', },
        name="login"),

    url('^logout$',
        auth_views.logout,
        { 'next_page': '/' },
        name="logout"),

    url(r'^register$', views.register, name='register'),

    url(r'^viewwriting/([a-zA-Z0-9_\-=]+)', views.view_writing, name='viewwriting'),

    url(r'^write$', views.write, name='write'),
]
