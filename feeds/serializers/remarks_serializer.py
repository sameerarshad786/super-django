from rest_framework import serializers

from ..models import Remarks


class RemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remarks
        fields = (
            "id", "user", "on_post", "on_comment", "popularity",
            "created", "updated"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "on_comment": {"required": False}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        return Remarks.objects.create(user=user, **validated_data)
