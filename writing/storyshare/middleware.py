import pytz

from django.utils import timezone

class TimezoneMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            tzname = request.user.userinfo.timezone
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
