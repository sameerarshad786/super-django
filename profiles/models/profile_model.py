from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from core.models.core_model import UUID
from core.models.user_model import User


def profile_photo_path(instance, filename):
    return f"profile/{instance.id}/{filename}"


def cover_photo_path(instance, filename):
    return f"cover/{instance.id}/{filename}"


class Profile(UUID):
    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")

    user_gender = models.CharField(
        max_length=10, choices=Gender.choices
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    username = models.CharField(
        max_length=15
    )
    profile_image = models.ImageField(
        upload_to=profile_photo_path
    )
    cover_image = models.ImageField(
        upload_to=cover_photo_path, default="cover/default.png"
    )
    phone_number = PhoneNumberField(blank=True)
    about = models.TextField()

    def __str__(self) -> str:
        return f"{self.user}"
