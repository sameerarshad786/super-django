from django.db import models

from core.mixins import UUID
from core.models import User
from .product_model import Products


class Cart(UUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
