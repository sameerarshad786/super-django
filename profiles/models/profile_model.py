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


class Profile(UUID):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")

    gender = models.CharField(max_length=10, choices=Gender.choices)

    username = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=25, blank=True)
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

    class Education(models.TextChoices):
        METRIC = "metric", _("Metric")
        INTERMEDIATE = "intermediate", _("Intermediate")
        BACHELORS = "bachelors", _("Bachelors")
        MASTERS = "masters", _("Masters")
        PHD = "phd", _("Phd")

    education = models.CharField(
        max_length=24, choices=Education.choices, blank=True
    )

    class CurrentStatus(models.TextChoices):
        SINGLE = "single", _("Single")
        MARRIED = "married", _("Married")
        UNMARRIED = "unmarried", _("Unmarried")
        DIVORCE = "divorce", _("Divorce")
        WIDOW = "widow", _("Widow")
        WIDOWER = "widower", _("Widower")

    current_status = models.CharField(
        max_length=18, choices=CurrentStatus.choices, blank=True
    )

    class EmploymentStatus(models.TextChoices):
        STUDENT = "student", _("Student")
        WORKER = "worker", _("worker")
        EMPLOYEE = "employee", _("Employee")
        SELFEMPLOYED = "self-employed", _("Self-Employed")

    employment_status = models.CharField(
        max_length=26, choices=EmploymentStatus.choices, blank=True,
    )

    profession = models.CharField(max_length=100, blank=True)
    location = models.JSONField(blank=True, null=True)
