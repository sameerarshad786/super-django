import uuid

from django.db import models
from django.utils import timesince


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

    def created(self):
        splitting = str(timesince.timesince(self.created_at))
        return f"{splitting.split(',')[0]}"

    def updated(self):
        splitting = str(timesince.timesince(self.updated_at))
        return f"{splitting.split(',')[0]}"
