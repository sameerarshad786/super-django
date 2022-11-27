from datetime import timedelta

from django.utils import timesince, timezone
from django.db.models import Q, Value, Case, When
from django.db.models.functions import Concat, Extract
from django.db import models


def get_timesince(time):
    created = timesince.timesince(time).split(", ")[0]
    x = timezone.now() - time
    if int(x.total_seconds()) <= timedelta(seconds=10).seconds:
        return "just now"
    elif int(x.total_seconds()) <= timedelta(seconds=59).seconds:
        return f"{int(x.total_seconds())} seconds ago"
    return f"{created} ago"


created_ = Case(
    When(
        Q(created__gte=timedelta(seconds=1))
        & ~Q(created__gte=timedelta(minutes=1)), then=Concat(
            Extract("created", "second"),
            Value(" second ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(created__gte=timedelta(minutes=1))
        & ~Q(created__gte=timedelta(minutes=60)), then=Concat(
            Extract("created", "minute"),
            Value(" minute ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(created__gte=timedelta(hours=1))
        & ~Q(created__gte=timedelta(hours=24)), then=Concat(
            Extract("created", "hour"),
            Value(" hour ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(created__gte=timedelta(days=1))
        & ~Q(created__gte=timedelta(days=365)), then=Concat(
            Extract("created", "day"),
            Value(" day ago"),
            output_field=models.CharField()
        )
    )
)

updated_ = Case(
    When(
        Q(updated__gte=timedelta(seconds=60))
        & ~Q(updated__gte=timedelta(minutes=1)), then=Concat(
            Extract("updated", "second"),
            Value(" second ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(updated__gte=timedelta(minutes=1))
        & ~Q(updated__gte=timedelta(minutes=60)), then=Concat(
            Extract("updated", "minute"),
            Value(" minute ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(updated__gte=timedelta(hours=1))
        & ~Q(updated__gte=timedelta(hours=24)), then=Concat(
            Extract("updated", "hour"),
            Value(" hour ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(updated__gte=timedelta(days=1))
        & ~Q(updated__gte=timedelta(days=365)), then=Concat(
            Extract("updated", "day"),
            Value(" day ago"),
            output_field=models.CharField()
        )
    ),
)
