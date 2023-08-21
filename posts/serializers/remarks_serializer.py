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

    def validate(self, attrs):
        request = self.context["request"]
        post_id = self.context.get("post_id")
        fields = ["like", "heart", "funny", "insightful", "disappoint"]
        field_dict = {field: False for field in fields}
        final_data = {**field_dict, **attrs}
        true_count = sum(1 for value in final_data.values() if value is True)
        if true_count == 1:
            if Remarks.objects.filter(
                user=request.user, post_id=post_id
            ).exists() and request.method == "POST":
                raise serializers.ValidationError(_("Entry already exists"))
            if self.instance.comment != attrs.get("comment"):
                raise serializers.ValidationError(_("No action found"))
        else:
            raise serializers.ValidationError(_("You can only give 1 action"))
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        post_id = self.context.get("post_id")
        return Remarks.objects.create(
            user=user, post_id=post_id, **validated_data)

    def update(self, instance, validated_data):
        fields = ["like", "heart", "funny", "insightful", "disappoint"]
        result = [field for field in fields if validated_data.keys()]
        field_dict = {field: False for field in result}
        for x, y in {**field_dict, **validated_data}.items():
            setattr(instance, x, y)
        instance.save()
        return instance
