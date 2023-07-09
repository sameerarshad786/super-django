from django.db import models
from core.mixins import UUID


def scraped_source_icon_media_path(instance, filename):
    return f"scraped-source-icon/{instance.id}/{filename}"


class ProductSource(UUID):
    name = models.CharField(max_length=155)
    domain = models.URLField(unique=True)
    icon = models.ImageField(
        upload_to=scraped_source_icon_media_path, unique=True)
