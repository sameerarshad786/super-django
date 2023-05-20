from django.db import models

from core.mixins import UUID
from core.models import User


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
    message = models.TextField()
