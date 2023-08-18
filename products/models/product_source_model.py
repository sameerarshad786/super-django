from django.db import models
from core.mixins import UUID


class ProductSource(UUID):
    name = models.CharField(max_length=155)
    domain = models.URLField(unique=True)
    icon = models.URLField(unique=True)
