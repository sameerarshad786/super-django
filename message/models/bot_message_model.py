from django.db import models

from core.mixins import UUID
from core.models import User


class BotMessages(UUID):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    discussion = models.JSONField(default=list)
