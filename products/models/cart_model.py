from django.db import models

from core.mixins import UUID
from core.models import User


class Cart(UUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.UUIDField(primary_key=False, editable=True)
    quantity = models.PositiveIntegerField(default=1)
