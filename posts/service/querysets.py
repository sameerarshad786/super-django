import os

from datetime import timedelta

from django.db.models import F, Value, When, Case, Q
from django.db.models.functions import Concat, Extract
from django.db import models
from django.conf import settings


created_ = Case(
    When(
        Q(created__gte=timedelta(seconds=59))
        & ~Q(created__gte=timedelta(minutes=1)), then=Concat(
            Extract("created", "second"),
            Value(" seconds ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(created__lt=timedelta(minutes=2)), then=Value("1 minute ago")
    ),
    When(
        Q(created__gte=timedelta(minutes=1))
        & ~Q(created__gte=timedelta(minutes=60)), then=Concat(
            Extract("created", "minute"),
            Value(" minutes ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(created__lt=timedelta(hours=2)), then=Value("1 hour ago")
    ),
    When(
        Q(created__gte=timedelta(hours=1))
        & ~Q(created__gte=timedelta(hours=24)), then=Concat(
            Extract("created", "hour"),
            Value(" hours ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(created__lt=timedelta(days=2)), then=Value("1 day ago")
    ),
    When(
        Q(created__gte=timedelta(days=1))
        & ~Q(created__gte=timedelta(days=365)), then=Concat(
            Extract("created", "day"),
            Value(" days ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(created__lt=timedelta(days=732)), then=Value("1 year ago")
    ),
    When(
        Q(created__gte=timedelta(days=732)), then=Concat(
            Extract("created_at", "year"),
            Value(" years ago"),
            output_field=models.CharField()
        )
    )
)

updated_ = Case(
    When(
        Q(updated__gte=timedelta(seconds=60))
        & ~Q(updated__gte=timedelta(minutes=1)), then=Concat(
            Extract("updated", "second"),
            Value(" seconds ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(updated__lt=timedelta(minutes=2)), then=Concat(
            Extract("updated", "minute"),
            Value(" minute ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(updated__gte=timedelta(minutes=1))
        & ~Q(updated__gte=timedelta(minutes=60)), then=Concat(
            Extract("updated", "minute"),
            Value(" minutes ago"),
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
        Q(updated__lt=timedelta(days=2)), then=Concat(
            Extract("updated", "day"),
            Value(" day ago"),
            output_field=models.CharField()
        )
    ),
    When(
        Q(updated__gte=timedelta(days=1))
        & ~Q(created__gte=timedelta(days=365)), then=Concat(
            Extract("updated", "day"),
            Value(" days ago"),
            output_field=models.CharField()
        )
    )
)

Posts_image = Concat(
    Value(settings.MEDIA_BUCKET_URL),
    F("files"),
    output_field=models.URLField()
)

profile_picture = Concat(
    Value(settings.MEDIA_BUCKET_URL),
    F("user__profile__profile_image"),
    output_field=models.URLField()
)

cover_picture = Concat(
    Value(settings.MEDIA_BUCKET_URL),
    F("user__profile__cover_image"),
    output_field=models.URLField()
)

profile_link = Concat(
    Value(settings.PROFILE_URL),
    F("user__profile__username"),
    output_field=models.URLField()
)
