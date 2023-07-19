from django.contrib.gis.db import models

from . import User
from core.mixins import UUID


class UserSensitiveInformation(UUID):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    point = models.PointField(null=True, blank=False)
