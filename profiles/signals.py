from django.db.models.signals import pre_save
from django.dispatch import receiver

from profiles.models.profile_model import Profile
from core.models.user_model import User


@receiver(pre_save, sender=User)
def create_profile_of_verified_users(sender, instance, **kwargs):
    if instance.is_verified and User.objects.filter(pk=instance.pk, is_verified=False).exists():
        Profile.objects.create(user=instance)
