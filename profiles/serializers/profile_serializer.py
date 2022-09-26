from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from profiles.models.profile_model import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id", "user", "username", "user_gender", "phone_number",
            "profile_image", "cover_image", "about", "created", "updated"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "username": {"required": False},
            "about": {"required": False}
        }

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user == instance.user:
            return super().update(instance, validated_data)
        raise serializers.ValidationError(_(
            "you cant update someone profile"
        ))
