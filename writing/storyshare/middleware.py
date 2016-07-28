import pytz

from django.utils import timezone

class TimezoneMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            tzname = request.user.preferences.timezone
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
