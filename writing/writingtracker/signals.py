from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from writingtracker.models import UserInfo


@receiver(post_save, sender=User)
def create_userinfo(sender, **kwargs):
    user = kwargs['instance']

    if kwargs['created']:
        ui = UserInfo(
            last_reset=timezone.now(),
            num_words=500,
            timezone='US/Eastern',
            user=user
        )

        ui.save()
