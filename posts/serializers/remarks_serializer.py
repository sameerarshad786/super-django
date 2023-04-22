from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..models import Remarks


class RemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remarks
        fields = (
            "id",
            "user",
            "post",
            "comment",
            "popularity",
            "created_at",
            "updated_at"
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        if Remarks.objects.filter(user=user).exists():
            raise serializers.ValidationError(_("Entry already exists"))
        return Remarks.objects.create(user=user, **validated_data)
