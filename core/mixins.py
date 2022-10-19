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
        splitting = timesince.timesince(self.created_at).split(", ")[0]
        return splitting

    def updated(self):
        splitting = timesince.timesince(self.updated_at).split(", ")[0]
        return splitting
