from rest_framework import serializers

from ..models import UserSensitiveInformation
from core.custom_serializer_fields import PointSerializer


class UserSensitiveInformationSerializer(serializers.ModelSerializer):
    point = PointSerializer()

    class Meta:
        model = UserSensitiveInformation
        fields = ("id", "user", "point")
        extra_kwargs = {
            "user": {"read_only": True}
        }
