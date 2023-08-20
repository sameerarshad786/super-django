from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..models import Remarks
from profiles.serializers import UserSerializer


class RemarkSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Remarks
        fields = (
            "id",
            "user",
            "post",
            "comment",
            "like",
            "heart",
            "funny",
            "insightful",
            "disappoint",
            "created",
            "updated"
        )
        extra_kwargs = {
            "post": {"read_only": True}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        post_id = self.context.get("post_id")
        if Remarks.objects.filter(user=user, post_id=post_id).exists():
            raise serializers.ValidationError(_("Entry already exists"))
        return Remarks.objects.create(
            user=user, post_id=post_id, **validated_data)

    def update(self, instance, validated_data):
        fields = ["like", "heart", "funny", "insightful", "disappoint"]
        result = [field for field in fields if next(iter(validated_data.keys()))] # noqa
        field_dict = {field: False for field in result}
        for x, y in {**field_dict, **validated_data}.items():
            setattr(instance, x, y)
        instance.save()
        return instance
