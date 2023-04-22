from django.conf import settings

from rest_framework import serializers

from profiles.models.profile_model import Profile
from core.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "username",
            "gender",
            "full_name",
            "phone_number",
            "profile_image",
            "cover_image",
            "is_private",
            "skills",
            "education",
            "current_status",
            "employment_status",
            "profession",
            "location",
            "created",
            "updated"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "username": {"required": False},
            "about": {"required": False},
            "profile_image": {"required": False},
            "profession": {"required": False},
            "location": {"read_only": True}
        }

    def update(self, instance, validated_data):
        profile_image = validated_data.get("profile_image")
        gender = validated_data.get("gender")
        if instance.username == "" and validated_data.get("username") is None:
            validated_data.update(username=instance.id)
        if profile_image is None:
            if gender == Profile.Gender.MALE:
                validated_data.update(profile_image="profile/male.png")
            elif gender == Profile.Gender.FEMALE:
                validated_data.update(profile_image="profile/female.png")
        return super().update(instance, validated_data)


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "user", "profile_image")
        extra_kwargs = {
            "user": {"read_only": True},
            "profile_image": {"required": False}
        }

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if instance.gender == Profile.Gender.MALE:
            return Profile.objects.filter(user=user).update(
                profile_image="profile/male.png"
            )
        elif instance.gender == Profile.Gender.FEMALE:
            return Profile.objects.filter(user=user).update(
                cover_image="profile/female.png"
            )

        return super().update(instance, validated_data)


class CoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "user", "cover_image")
        extra_kwargs = {
            "user": {"read_only": True},
            "profile_image": {"required": False}
        }

    def update(self, instance, validated_data):
        user = self.context["request"].user
        return Profile.objects.filter(user=user).update(
            cover_image="cover/default-cover.png"
        )


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.profile.full_name")
    profile_image = serializers.ImageField(
        source="user.profile.profile_image")
    cover_image = serializers.ImageField(source="user.profile.cover_image")
    profile_link = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("full_name", "profile_image", "cover_image", "profile_link")

    def get_profile_link(self, obj):
        return f"{settings.PROFILE_URL}{obj.user.profile.username}/"
