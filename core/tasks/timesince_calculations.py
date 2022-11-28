from datetime import timedelta

from django.utils import timesince, timezone


def get_timesince(time):
    created = timesince.timesince(time).split(", ")[0]
    x = timezone.now() - time
    if int(x.total_seconds()) <= timedelta(seconds=10).seconds:
        return "just now"
    elif int(x.total_seconds()) <= timedelta(seconds=59).seconds:
        return f"{int(x.total_seconds())} seconds ago"
    return f"{created} ago"
