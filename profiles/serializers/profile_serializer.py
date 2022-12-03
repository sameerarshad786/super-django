from rest_framework import serializers

from profiles.models.profile_model import Profile, Gender


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
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
            if gender == Gender.MALE:
                validated_data.update(profile_image="profile/male.png")
            elif gender == Gender.FEMALE:
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
        if instance.gender == Gender.MALE:
            return Profile.objects.filter(user=user).update(
                profile_image="profile/male.png"
            )
        elif instance.gender == Gender.FEMALE:
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
