from datetime import timedelta
import uuid

from django.db import models
from django.utils import timesince, timezone


class UUID(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def created(self):
        created = timesince.timesince(self.created_at).split(", ")[0]
        x = timezone.now() - self.created_at
        if int(x.total_seconds()) <= timedelta(seconds=10).seconds:
            return "just now"
        elif int(x.total_seconds()) <= timedelta(seconds=59).seconds:
            return f"{int(x.total_seconds())} seconds ago"
        return f"{created} ago"

    def updated(self):
        updated = timesince.timesince(self.updated_at).split(", ")[0]
        x = timezone.now() - self.updated_at
        if int(x.total_seconds()) <= timedelta(seconds=59).seconds:
            return f"updated {int(x.total_seconds())} seconds ago"
        return f"{updated} ago"
