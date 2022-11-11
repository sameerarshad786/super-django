from rest_framework import serializers

from profiles.models.profile_model import Profile, Gender


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id", "user", "username", "user_gender", "profile_image",
            "cover_image", "about", "phone_number", "skills", "education",
            "current_status", "is_private", "created", "updated"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "about": {"required": False},
            "profile_image": {"required": False}
        }

    def update(self, instance, validated_data):
        profile_image = validated_data.get("profile_image")
        user_gender = validated_data.get("user_gender")
        if profile_image is None:
            if user_gender == Gender.MALE:
                validated_data.update(profile_image="profile/male.png")
            elif user_gender == Gender.FEMALE:
                validated_data.update(profile_image="profile/female.png")
        return super().update(instance, validated_data)


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id", "user", "profile_image"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "profile_image": {"required": False}
        }

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if instance.user_gender == Gender.MALE:
            return Profile.objects.filter(user=user).update(
                profile_image="profile/male.png"
            )
        elif instance.user_gender == Gender.FEMALE:
            return Profile.objects.filter(user=user).update(
                cover_image="profile/female.png"
            )

        return super().update(instance, validated_data)


class CoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id", "user", "cover_image"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "profile_image": {"required": False}
        }

    def update(self, instance, validated_data):
        user = self.context["request"].user
        return Profile.objects.filter(user=user).update(
            cover_image="cover/default-cover.png"
        )
