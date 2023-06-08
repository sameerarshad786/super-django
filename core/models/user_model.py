from datetime import timedelta

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
    PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timesince, timezone

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
    email = models.EmailField(max_length=50, unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deactivate_by_admin = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken().for_user(self)
        return {
            "refresh": str(refresh),
            "access_token": str(refresh.access_token)
        }

    def joined(self):
        created = timesince.timesince(self.created_at).split(", ")[0]
        x = timezone.now() - self.created_at
        if int(x.total_seconds()) <= timedelta(seconds=10).seconds:
            return "just now"
        elif int(x.total_seconds()) <= timedelta(seconds=59).seconds:
            return f"{int(x.total_seconds())} seconds ago"
        return f"{created} ago"

    def updated(self):
        updated = timesince.timesince(self.updated_at).split(", ")[0]
        x = timezone.now() - self.updated_at
        if int(x.total_seconds()) <= timedelta(seconds=59).seconds:
            return f"updated {int(x.total_seconds())} seconds ago"
        return f"{updated} ago"
