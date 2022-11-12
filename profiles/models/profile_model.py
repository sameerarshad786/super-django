from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from phonenumber_field.modelfields import PhoneNumberField

from core.mixins import UUID
from core.models.user_model import User


def profile_photo_path(instance, filename):
    return f"profile/{instance.id}/{filename}"


def cover_photo_path(instance, filename):
    return f"cover/{instance.id}/{filename}"


class Gender(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")


class Education(models.TextChoices):
    METRIC = "metric", _("Metric")
    INTERMEDIATE = "intermediate", _("Intermediate")
    BACHELORS = "bachelors", _("Bachelors")
    MASTERS = "masters", _("Masters")
    PHD = "phd", _("Phd")


class CurrentStatus(models.TextChoices):
    SINGLE = "single", _("Single")
    MARRIED = "married", _("Married")
    UNMARRIED = "unmarried", _("Unmarried")
    DIVORCE = "divorce", _("Divorce")
    WIDOW = "widow", _("Widow")
    WIDOWER = "widower", _("Widower")


class Profile(UUID):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    username = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to=profile_photo_path)
    cover_image = models.ImageField(
        upload_to=cover_photo_path, default="cover/default.png"
    )
    phone_number = PhoneNumberField(blank=True)
    about = models.TextField()
    skills = ArrayField(
        models.CharField(max_length=255), size=5, blank=True, null=True
    )
    education = models.CharField(
        max_length=24, choices=Education.choices, blank=True, null=True
    )
    current_status = models.CharField(
        max_length=18, choices=CurrentStatus.choices, blank=True, null=True
    )
    is_private = models.BooleanField(default=False)
