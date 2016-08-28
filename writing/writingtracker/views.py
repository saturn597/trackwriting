from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
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
import json
import math
import pytz


def index(request):
    context = {}
    user = request.user

    if not user.is_authenticated():
        return render(request, 'writingtracker/landing.html')

    else:
        per_page = settings.SHORT_RESULTS_PER_PAGE

        userinfo = user.userinfo

        current_user_date = get_current_user_date(user)

        period = [
            current_user_date,
            current_user_date - datetime.timedelta(days=1)
        ]

        # reset the current streak if user hasn't met their goal lately
        if userinfo.last_goal_met not in period:
            userinfo.current_streak = 0
            userinfo.save()

        daily_words, no_more_daily = get_daily_wordcount(user, 0, per_page)
        words_today = daily_words[current_user_date]

        recents, no_more_writings = get_past_writings(user, 0, per_page)

        context = {
            'today': current_user_date,
            'todays_wordcount': words_today,

            'words_by_day': daily_words,
            'recents': recents,
            'no_more_daily': no_more_daily,
            'no_more_writings': no_more_writings,

            'goal': userinfo.num_words,
            'words_left': userinfo.num_words - words_today,

            'current_streak': userinfo.current_streak,
            'longest_streak': userinfo.longest_streak,
        }

    return render(request, 'writingtracker/index.html', context)


def get_daily_wordcount(user, page, step):
    userinfo = user.userinfo

    page = int(page)

    tz = pytz.timezone(userinfo.timezone)
    current_user_date = get_current_user_date(user)

    last_reset_userdate = get_date(userinfo.last_reset, tz)
    days_since_reset = (current_user_date - last_reset_userdate).days + 1
    days_since_reset = max(days_since_reset, 0)

    max_page = math.ceil(days_since_reset / step) - 1

    start = step * page
    end = step * (page + 1)

    # construct a list of days representing the current period
    period = [
        current_user_date - datetime.timedelta(days=x)
        for x in range(start, end)
    ]

    period = [date for date in period if date >= last_reset_userdate]

    # get the writings from the current period
    period_writings = Writing.objects.filter(
        author=user,
        user_date__in=period
    ).exclude(
        time__lt=userinfo.last_reset
    )

    # How many words did the user complete for each day in the period?
    words_by_day = OrderedDict.fromkeys(period, 0)
    for w in period_writings:
        words_by_day[w.user_date] += len(w.text.split())

    return words_by_day, page >= max_page


@login_required
def paged_daily_history(request, page):
    user = request.user
    page = int(page)
    per_page = settings.LONG_RESULTS_PER_PAGE

    words_by_day, no_more = get_daily_wordcount(user, page, per_page)

    current_user_date = get_current_user_date(user)

    fmt = '%b. %d, %Y'
    daily_history = [{
        'date': d.strftime(fmt),
        'success': words_by_day[d] >= user.userinfo.num_words,
        'today': d == current_user_date,
    } for d in words_by_day]

    result = {
        'noMore': no_more,
        'content': daily_history,
    }

    return HttpResponse(json.dumps(result))


def get_past_writings(user, page, step):
    writings = Writing.objects.filter(
        author=user).order_by(
        '-time')

    count = writings.count()
    max_page = math.ceil(count / step) - 1

    start = step * page
    end = step * (page + 1)
    past_writings = writings[start:end]

    return past_writings, page >= max_page


@login_required
def paged_past_writings(request, page):
    user = request.user
    page = int(page)
    per_page = settings.LONG_RESULTS_PER_PAGE

    past_writings, no_more = get_past_writings(user, page, per_page)

    fmt = '%b %d, %Y, %I:%M %p'
    result = {
        'noMore': no_more,
        'content': [{
            'title': w.title,
            'time': timezone.localtime(w.time).strftime(fmt),
            'urlId': w.url_id,
        } for w in past_writings]}

    return HttpResponse(json.dumps(result))


def past_writings(request):
    return render(request, 'writingtracker/pastwritings.html')


def daily_history(request):
    return render(request, 'writingtracker/dailyhistory.html')


@login_required
def preferences(request):
    userinfo = request.user.userinfo
    prefs_form = PreferencesForm(instance=userinfo)

    if request.POST:
        prefs_form = PreferencesForm(request.POST, instance=userinfo)

        if prefs_form.is_valid():
            prefs_form.save()

            userinfo.last_reset = timezone.now()
            userinfo.last_goal_met = None
            userinfo.save()

            return HttpResponseRedirect(reverse('writingtracker:index'))

    return render(
        request,
        'writingtracker/preferences.html',
        {'form': prefs_form}
    )


def register(request):
    prefs_form = PreferencesForm(initial={'timezone': 'US/Eastern', })
    user_creation_form = UserCreationForm()

    if request.POST:

        user_creation_form = UserCreationForm(request.POST)
        prefs_form = PreferencesForm(request.POST)

        if user_creation_form.is_valid() and prefs_form.is_valid():
            user = user_creation_form.save()

            prefs_form = PreferencesForm(request.POST, instance=user.userinfo)
            prefs_form.save()

            authenticated_user = authenticate(
                username=user_creation_form.cleaned_data['username'],
                password=user_creation_form.cleaned_data['password1']
            )

            login(request, authenticated_user)

            return HttpResponseRedirect(reverse('writingtracker:index'))

    return render(request, 'writingtracker/register.html', {
        'user_creation_form': user_creation_form,
        'prefs_form': prefs_form,
    })


def view_writing(request, id):
    try:
        w = Writing.objects.get(url_id=id)
    except Writing.DoesNotExist:
        w = 'Whoops, not found!'
    return render(request, 'writingtracker/viewwriting.html', {'writing': w})


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
            writings_today = Writing.objects.filter(
                author=story.author,
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

            return HttpResponseRedirect(reverse('writingtracker:index'))

    return render(request, 'writingtracker/write.html', {'form': form})


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
