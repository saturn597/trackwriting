from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

import base64
import uuid

class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    num_words = models.PositiveIntegerField()

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

    def __str__(self):
        return '%s by %s' % (self.title, self.author.username)
