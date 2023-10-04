from .models import Products
from django.db.models.signals import post_save
from django.dispatch import receiver

from products.document import ProductIndex


@receiver(post_save, sender=Products)
def index_post(sender, instance, **kwargs):
    obj = ProductIndex(
        meta={'id': instance.id},
        name=instance.name,
        description=instance.description
    )
    obj.save()
    return obj.to_dict(include_meta=True)
