from __future__ import unicode_literals

from django.apps import AppConfig


class WritingtrackerConfig(AppConfig):
    name = 'writingtracker'

    def ready(self):
        import writingtracker.signals  # noqa
