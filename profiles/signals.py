from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver

from profiles.models.profile_model import Profile
from core.models.user_model import User


@receiver(pre_save, sender=User)
def create_profile_of_verified_users(sender, instance, **kwargs):
    if Profile.objects.filter(user=instance.pk).exists():
        Profile.objects.filter(user=instance)

    elif instance.is_verified and User.objects.filter(
        pk=instance.pk, is_verified=False).exists():
        Profile.objects.create(user=instance)
