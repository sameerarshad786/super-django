from django.db import models

from core.mixins import UUID
from core.models import User


class BotKeyErrors(UUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    error = models.TextField()
    resolved = models.BooleanField(default=False)
