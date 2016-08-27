from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'storyshare'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^register$', views.register, name='register'),

    url('^login$',
        auth_views.login,
        {'template_name': 'storyshare/login.html', },
        name="login"),

    url('^logout$',
        auth_views.logout,
        {'next_page': '/', },
        name="logout"),

    url(r'^preferences$', views.preferences, name='preferences'),

    url(r'^write$', views.write, name='write'),

    url(r'^pastwritings/([0-9]+)$',
        views.paged_past_writings,
        name='pagedpastwritings'),

    url(r'^dailyhistory/([0-9]+)$',
        views.paged_daily_history,
        name='pageddailyhistory'),

    url(r'^pastwritings$', views.past_writings, name='pastwritings'),
    url(r'^dailyhistory$', views.daily_history, name='dailyhistory'),

    url(r'^viewwriting/([a-zA-Z0-9_\-=]+)$',
        views.view_writing,
        name='viewwriting'),
]
