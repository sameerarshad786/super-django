from django.db.models.signals import pre_delete
from django.dispatch import receiver

from products.models import Products, Cart


@receiver(pre_delete, sender=Products)
def product_on_delete_cart(sender, instance, **kwargs):
    product_on_cart = Cart.objects.get(product=instance.id)
    product_on_cart.delete()
