from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from friendship.models import Follow, Block

from core.tasks import get_timesince


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("follower", "followee", "created")
        extra_kwargs = {
            "follower": {"read_only": True},
            "created": {"read_only": True}
        }

    def to_representation(self, instance):
        request = self.context["request"]
        data = dict()
        data["id"] = instance.id
        if instance.followee == request.user:
            data["user_id"] = instance.follower.id
            data["username"] = instance.follower.profile.username
            data["email"] = instance.follower.email
            data["profile_image"] = request.build_absolute_uri(
                instance.follower.profile.profile_image.url
            )
        elif instance.follower == request.user:
            data["user_id"] = instance.followee.id
            data["username"] = instance.followee.profile.username
            data["email"] = instance.followee.email
            data["profile_image"] = request.build_absolute_uri(
                instance.followee.profile.profile_image.url
            )
        data["created"] = get_timesince(instance.created)
        return data

    def validate(self, attrs):
        follower = self.context["request"].user
        followee = attrs["followee"]

        if not follower.profile.username:
            raise serializers.ValidationError(_("Update your profile first"))

        if follower == followee:
            raise serializers.ValidationError(_("You can't follow your self"))

        if Follow.objects.filter(
            follower=follower, followee=followee
        ).exists():
            raise serializers.ValidationError(_("already followed"))

        if Block.objects.filter(blocker=follower, blocked=followee):
            raise serializers.ValidationError(_("you blocked this user"))

        if Block.objects.filter(blocker=followee, blocked=follower):
            raise serializers.ValidationError(_("user blocked you"))

        return attrs

    def create(self, validated_data):
        follower = self.context["request"].user
        return Follow.objects.add_follower(
            follower, **validated_data
        )
