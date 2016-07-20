from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

import base64
import uuid

class Writing(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    url_id = models.CharField(
            max_length=10,
            unique=True,)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
