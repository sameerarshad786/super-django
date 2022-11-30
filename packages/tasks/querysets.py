from datetime import timedelta

from django.db.models import F, Value, When, Case, Q
from django.db.models.functions import Concat, Extract
from django.db import models


created_ = Case(
    When(
        Q(created_at__gte=timedelta(seconds=1))
        & ~Q(created_at__gte=timedelta(minutes=1)), then=Concat(
            Extract("created_at", "second"),
            Value(" seconds ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(created_at__lt=timedelta(minutes=2)), then=Value("1 minute ago")
    ),
    When(
        Q(created_at__gte=timedelta(minutes=1))
        & ~Q(created_at__gte=timedelta(minutes=60)), then=Concat(
            Extract("created_at", "minute"),
            Value(" minutes ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(created_at__lt=timedelta(hours=2)), then=Value("1 hour ago")
    ),
    When(
        Q(created_at__gte=timedelta(hours=1))
        & ~Q(created_at__gte=timedelta(hours=24)), then=Concat(
            Extract("created_at", "hour"),
            Value(" hours ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(created_at__lt=timedelta(days=2)), then=Value("1 day ago")
    ),
    When(
        Q(created_at__gte=timedelta(days=1))
        & ~Q(created_at__gte=timedelta(days=365)), then=Concat(
            Extract("created_at", "day"),
            Value(" days ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(created_at__lt=timedelta(days=730)), then=Value("1 year ago")
    ),
    When(
        Q(created_at__gte=timedelta(days=730)), then=Concat(
            F("created__year"),
            Value(" years ago"),
            output_field=models.CharField()
        )
    )
)
