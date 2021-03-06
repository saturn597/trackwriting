# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-31 17:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writingtracker', '0010_auto_20160731_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='longest_streak',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='current_streak',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='last_goal_met',
            field=models.DateField(default=datetime.date(2016, 7, 31)),
        ),
    ]
