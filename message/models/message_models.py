from django.db import models

from core.mixins import UUID
from core.models import User
from .conversation_model import Conversation


def messages_file_path(instance, filename):
    return f"message/{instance.id}/{filename}"


class Messages(UUID):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="from_user"
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="to_user"
    )
    message = models.TextField(blank=False)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True)
    is_seen = models.BooleanField(default=False)
    conversation_on = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to=messages_file_path, blank=True, null=True)

    def get_message(self):
        if len(self.message) > 30:
            return f"{self.message[:30]}..."
        return self.message
