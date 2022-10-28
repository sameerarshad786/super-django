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
            "about": {"required": False},
            "profile_image": {"required": False}
        }

    def update(self, instance, validated_data):
        profile_image = validated_data.get("profile_image")
        cover_image = validated_data.get("cover_image")
        user_gender = validated_data.get("user_gender")
        if profile_image is None:
            if user_gender == Profile.Gender.MALE:
                validated_data.update(profile_image="profile/male.png")
            elif user_gender == Profile.Gender.FEMALE:
                validated_data.update(profile_image="profile/female.png")

        if cover_image is None:
            validated_data.update(cover_image="cover/default-cover.png")

        return super().update(instance, validated_data)
