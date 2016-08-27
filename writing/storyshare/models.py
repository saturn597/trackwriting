from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

import pytz

MAX_TZ_LENGTH = max([len(tz) for tz in pytz.common_timezones])

TIMEZONE_CHOICES = [[tz, tz] for tz in pytz.common_timezones]


class UserInfo(models.Model):
    current_streak = models.PositiveIntegerField(default=0)

    last_reset = models.DateTimeField()

    # The date the user last completed their goal (in user-local time)
    last_goal_met = models.DateField(blank=True, null=True)

    longest_streak = models.PositiveIntegerField(default=0)

    num_words = models.PositiveIntegerField()

    timezone = models.CharField(
        max_length=MAX_TZ_LENGTH,
        choices=TIMEZONE_CHOICES)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Preferences for %s' % self.user.username


class Writing(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)

    url_id = models.CharField(
        max_length=10,
        unique=True,
    )

    # The date the writing was completed in user-local time
    user_date = models.DateField()

    def __str__(self):
        return '%s by %s' % (self.title, self.author.username)
