from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .forms import PreferencesForm, WritingForm
from .models import Writing

from base64 import urlsafe_b64encode
from uuid import uuid4

import datetime

def get_date(date_time, tz):
    date = tz.normalize(date_time.astimezone(tz)).date()
    return date

def index(request):
    context = {}
    if request.user.is_authenticated():
        days_back = 7
        tz = timezone.get_current_timezone()
        current_user_date = get_date(timezone.now(), tz)

        context['recents'] = Writing.objects.filter(
            author=request.user).order_by(
            '-time')[:50]

        # construct a list of days representing the current period
        period = [current_user_date - datetime.timedelta(days=x)
                for x in range(0, days_back)]

        # get the writings from that period
        period_writings = Writing.objects.filter(
            author=request.user,
            user_date__in=period)

        context['daily_writings'] = []
        for date in period:
            writings = [w for w in period_writings if w.user_date == date]
            context['daily_writings'].append({
                'when': date,
                'writings': writings,
                'wordcount': sum(len(w.text.split()) for w in writings),
                })

    return render(request, 'storyshare/index.html', context)

def preferences(request):
    prefs_form = PreferencesForm(instance=request.user.preferences)
    success = False

    if request.POST:
        prefs_form = PreferencesForm(request.POST, instance=request.user.preferences)

        if prefs_form.is_valid():
            prefs_form.save()
            success = True

    return render(request, 'storyshare/preferences.html', {'form': prefs_form, 'success': success})

def register(request):
    prefs_form = PreferencesForm()
    user_creation_form = UserCreationForm()

    if request.POST:
        user_creation_form = UserCreationForm(request.POST)
        prefs_form = PreferencesForm(request.POST)

        if user_creation_form.is_valid() and prefs_form.is_valid():
            user = user_creation_form.save()
            prefs = prefs_form.save(commit=False)
            prefs.user = user
            prefs.save()
            user.save()
            return HttpResponseRedirect(reverse('storyshare:index'))

    return render(request, 'storyshare/register.html', {
            'user_creation_form': user_creation_form,
            'prefs_form': prefs_form,
        })

def view_writing(request, id):
    print(id)
    try:
        w = Writing.objects.get(url_id=id)
    except Writing.DoesNotExist:
        w = 'Whoops, not found!'
    return render(request, 'storyshare/viewwriting.html', {'writing': w})

def write(request):
    form = WritingForm()
    errors = []

    url_id = generate_url_id()

    if request.method == 'POST':
        form = WritingForm(request.POST)

        url_id = generate_url_id()

        if not url_id:
            # generate_url_id may return None if it can't find an unused id.
            form.add_error(None, 'Something odd happened! We recommend you save your'
                    ' work off site.')

        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.url_id = url_id
            story.save()
            return HttpResponseRedirect(reverse('storyshare:index'))

    return render(request, 'storyshare/write.html', {'form': form})


def generate_url_id():
    for _ in range(1, 10):
        url_id = urlsafe_b64encode(uuid4().bytes)[:5]
        if not Writing.objects.filter(url_id=url_id).exists():
            return url_id
    return None
