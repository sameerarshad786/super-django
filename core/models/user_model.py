from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
    PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timesince

from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise TypeError(_("User can't create without email"))

        if not password:
            raise TypeError(_("User can't create without password"))

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=50, unique=True, db_index=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=True
    )
    is_deactivate_by_admin = models.BooleanField(
        default=False
    )
    is_verified = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.email}"

    def tokens(self):
        refresh = RefreshToken().for_user(self)
        return {
            "refresh": str(refresh),
            "access_token": str(refresh.access_token)
        }

    def created(self):
        splitting = str(timesince.timesince(self.created_at))
        return f"joined {splitting.split(', ')[0]} ago"

    def updated(self):
        splitting = str(timesince.timesince(self.updated_at))
        return f"updated {splitting.split(', ')[0]} ago"
