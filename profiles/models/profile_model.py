from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from core.mixins import UUID
from core.models.user_model import User

from phonenumber_field.modelfields import PhoneNumberField


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


class EmploymentStatus(models.TextChoices):
    STUDENT = "student", _("Student")
    WORKER = "worker", _("worker")
    EMPLOYEE = "employee", _("Employee")
    SELFEMPLOYED = "self-employed", _("Self-Employed")


class Profile(UUID):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    username = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to=profile_photo_path)
    cover_image = models.ImageField(
        upload_to=cover_photo_path, default="cover/default-cover.png"
    )
    phone_number = PhoneNumberField(blank=True)
    about = models.TextField()
    is_private = models.BooleanField(default=False)
    skills = ArrayField(
        models.CharField(max_length=255), size=5, blank=True, null=True
    )
    education = models.CharField(
        max_length=24, choices=Education.choices, blank=True, null=True
    )
    current_status = models.CharField(
        max_length=18, choices=CurrentStatus.choices, blank=True, null=True
    )
    employment_status = models.CharField(
        max_length=26, choices=EmploymentStatus.choices, blank=True, null=True
    )
    profession = models.CharField(max_length=100)
    location = models.JSONField(blank=True, null=True)
