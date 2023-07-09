from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import DecimalRangeField
from django.core.validators import MaxValueValidator, MinValueValidator

from core.mixins import UUID
from core.validators import validate_file_size
from .product_source_model import ProductSource


def scraped_products_media_path(instance, filename):
    return f"scraped-products/{instance.id}/{filename}"


class ProductTypes(UUID):
    type = models.CharField(max_length=150, unique=True)
    valid_name = models.BooleanField(default=False)


class Products(UUID):
    class Condition(models.TextChoices):
        NOT_DEFINED = "not defined", _("Not Defined")
        NEW = "new", _("New")
        USED = "used", _("Used")
        OPEN_BOX = "open box", _("Open Box")
        REFURBISHED = "refurbished", _("Refurbished")
        DEAD = "dead", _("Dead")
    
    class Source(models.TextChoices):
        NOT_DEFINED = "not defined", _("Not Defined")
        AMAZON = "amazon", _("Amazon")
        EBAY = "ebay", _("Ebay")
        DARAZ = "daraz", _("Daraz")
        ALI_EXPRESS = "ali express", _("Ali Express")
        ALI_BABA = "ali baba", _("Ali Baba")
        OLX = "olx", _("olx")
    
    class Brand(models.TextChoices):
        NOT_DEFINED = "not defined", _("Not Defined")
        APPLE = "apple", _("Apple")
        SAMSUNG = "samsung", _("Samsung")
        GOOGLE = "google", _("Google")
        LG = "lg", _("LG")
        HUAWEI = "huawei", _("Huawei")
        HTC = "htc", _("HTC")
        ONEPLUS = "oneplus", _("OnePlus")
        BLACK_BERRY = "black berry", _("Black Berry")
        MOTOROLA = "motorola", _("Motorola")
        NOKIA = "nokia", _("Nokia")

    product_source = models.ForeignKey(
        ProductSource, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=500)
    description = models.TextField()
    brand = models.CharField(max_length=11, choices=Brand.choices)
    type = models.ForeignKey(
        ProductTypes, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(
        upload_to=scraped_products_media_path,
        max_length=100,
        validators=[validate_file_size]
    )
    url = models.URLField(unique=True, max_length=500)
    items_sold = models.PositiveIntegerField(default=0)
    ratings = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0,
        max_digits=2,
        decimal_places=1
    )
    condition = models.CharField(
        max_length=11,
        choices=Condition.choices,
        default=Condition.USED
    )
    original_price = models.DecimalField(
        default=0, max_digits=7, decimal_places=2)
    price = DecimalRangeField(default=(Decimal('0.00'), Decimal('0.00')))
    shipping_charges = models.DecimalField(
        default=0, max_digits=5, decimal_places=2)
    source = models.CharField(max_length=11, choices=Source.choices)
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(-100)], default=0)
