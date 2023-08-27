from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from core.mixins import UUID
from core.models import User


class ProductCheckout(UUID):
    class PayThrough(models.TextChoices):
        DIRECT = "direct", _("Direct")
        STRIPE = "stripe", _("Stripe")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.UUIDField(primary_key=False, editable=True)
    discounted = models.IntegerField(
        validators=[MinValueValidator(-100), MaxValueValidator(0)], default=0)
    pay_through = models.CharField(choices=PayThrough.choices)
