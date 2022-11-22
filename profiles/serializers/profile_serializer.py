from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from profiles.models.profile_model import Profile, Gender
from ..location import get_location


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id", "user", "username", "gender", "profile_image",
            "cover_image", "phone_number", "about", "is_private",
            "skills", "education", "current_status", "employment_status",
            "profession", "location", "created", "updated"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "username": {"required": False},
            "about": {"required": False},
            "profile_image": {"required": False},
            "profession": {"required": False},
            "location": {"read_only": True}
        }

    def to_representation(self, instance):
        request = self.context["request"]
        data = dict()
        profile = Profile.objects.select_related(
            "user"
        ).get(id=instance.id)
        data["id"] = profile.id
        data["user_id"] = profile.user.id
        data["username"] = profile.username
        data["email"] = profile.user.email
        data["gender"] = profile.gender
        data["profile_image"] = request.build_absolute_uri(
            profile.profile_image.url
        ) if profile.profile_image else None
        data["cover_image"] = request.build_absolute_uri(
            profile.cover_image.url
        ) if profile.cover_image else None
        data["phone_number"] = profile.phone_number
        data["about"] = profile.about
        data["skills"] = profile.skills
        data["education"] = profile.education
        data["current_status"] = profile.current_status
        data["address"] = profile.location
        data["created"] = profile.created()
        data["updated"] = profile.updated()
        data["joined"] = profile.user.joined()
        data["user updated"] = profile.user.updated()
        if not profile.is_private or profile.user == request.user:
            return data
        return {
                "id": data["id"],
                "user_id": data["user_id"],
                "username": data["username"],
                "message": "profile is private"
        }

    def update(self, instance, validated_data):
        request = self.context["request"]
        profile_image = validated_data.get("profile_image")
        gender = validated_data.get("gender")
        if instance.location is None:
            validated_data.update(location=get_location(request))
        if instance.username == "" and validated_data.get("username") is None:
            raise serializers.ValidationError(_("user should have username"))
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
