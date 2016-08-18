from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .forms import PreferencesForm, WritingForm
from .models import Writing

from base64 import urlsafe_b64encode
from collections import OrderedDict
from uuid import uuid4

import datetime
import pytz

def index(request):
    context = {}
    user = request.user

    if not user.is_authenticated():
        return render(request, 'storyshare/landing.html')

    else:
        userinfo = user.userinfo

        recents = Writing.objects.filter(
            author=user).order_by(
            '-time')[:10]

        tz = timezone.get_current_timezone()
        current_user_date = get_current_user_date(user)

        # We'll look at a period of 10 days, but don't look at dates earlier
        # than when the user last reset.
        last_reset_userdate = get_date(userinfo.last_reset, tz)
        days_since_reset = (current_user_date - last_reset_userdate).days
        days_since_reset = max(days_since_reset, 0)
        days_back = min(10, days_since_reset + 1)

        # construct a list of days representing the current period
        period = [current_user_date - datetime.timedelta(days=x)
                for x in range(0, days_back)]

        # reset the current streak if user hasn't met their goal lately
        if not userinfo.last_goal_met in period[0:2]:
            userinfo.current_streak = 0
            userinfo.save()

        # get the writings from the current period
        period_writings = Writing.objects.filter(
            author=request.user,
            user_date__in=period
        ).exclude(
            time__lt=userinfo.last_reset
        )

        # How many words did the user complete for each day in the period?
        words_by_day = OrderedDict.fromkeys(period, 0)
        for w in period_writings:
            words_by_day[w.user_date] += len(w.text.split())

        words_today = words_by_day[current_user_date]

        context = {
                'recents': recents,
                'today': current_user_date,
                'todays_wordcount': words_today,
                'words_by_day': words_by_day,
                'goal': userinfo.num_words,
                'words_left': userinfo.num_words - words_today,
                'current_streak': userinfo.current_streak,
                'longest_streak': userinfo.longest_streak,
        }

    return render(request, 'storyshare/index.html', context)

@login_required
def reset(request):
    userinfo = request.user.userinfo
    prefs_form = PreferencesForm(instance=userinfo)

    if request.POST:
        prefs_form = PreferencesForm(request.POST, instance=userinfo)

        if prefs_form.is_valid():
            prefs_form.save()

            userinfo.last_reset = timezone.now()
            userinfo.last_goal_met = None
            userinfo.longest_streak = 0
            userinfo.save()

            return HttpResponseRedirect(reverse('storyshare:index'))

    return render(request, 'storyshare/reset.html', {'form': prefs_form})

def register(request):
    prefs_form = PreferencesForm(initial={"timezone": "US/Eastern",})
    user_creation_form = UserCreationForm()

    if request.POST:

        user_creation_form = UserCreationForm(request.POST)
        prefs_form = PreferencesForm(request.POST)

        if user_creation_form.is_valid() and prefs_form.is_valid():
            user = user_creation_form.save()

            userinfo = prefs_form.save(commit=False)
            userinfo.last_reset = timezone.now()
            userinfo.user = user
            userinfo.save()

            return HttpResponseRedirect(reverse('storyshare:index'))

    return render(request, 'storyshare/register.html', {
            'user_creation_form': user_creation_form,
            'prefs_form': prefs_form,
        })

def view_writing(request, id):
    try:
        w = Writing.objects.get(url_id=id)
    except Writing.DoesNotExist:
        w = 'Whoops, not found!'
    return render(request, 'storyshare/viewwriting.html', {'writing': w})

@login_required
def write(request):
    form = WritingForm()

    url_id = generate_url_id()

    if request.method == 'POST':
        form = WritingForm(request.POST)

        url_id = generate_url_id()

        if not url_id:
            # generate_url_id may return None if it can't find an unused id.
            form.add_error(None, 'Something odd happened! We recommend you'
                    ' save your work off site.')

        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.user_date = get_current_user_date(story.author)
            story.url_id = url_id
            story.save()

            info = story.author.userinfo
            today = story.user_date
            yesterday = today - datetime.timedelta(days=1)

            # see if we met the goal for the day
            writings_today = Writing.objects.filter(author=story.author,
                    user_date=today)
            word_count_today = sum(len(w.text.split()) for w in writings_today)
            if word_count_today >= info.num_words:
                if not info.last_goal_met or info.last_goal_met < yesterday:
                    info.current_streak = 1
                if info.last_goal_met == yesterday:
                    info.current_streak += 1
                info.last_goal_met = today
                if info.current_streak > info.longest_streak:
                    info.longest_streak = info.current_streak

                info.save()

            return HttpResponseRedirect(reverse('storyshare:index'))

    return render(request, 'storyshare/write.html', {'form': form})

def generate_url_id():
    for _ in range(1, 10):
        url_id = urlsafe_b64encode(uuid4().bytes)[:5]
        if not Writing.objects.filter(url_id=url_id).exists():
            return url_id
    return None

def get_date(date_time, tz):
    date = tz.normalize(date_time.astimezone(tz)).date()
    return date

def get_current_user_date(user):
    tz = pytz.timezone(user.userinfo.timezone)
    return get_date(timezone.now(), tz)
