from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from friendship.models import FriendshipRequest, Friend, Block, Follow


class FriendShipRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendshipRequest
        fields = (
            "id", "from_user", "to_user", "viewed", "created"
        )
        extra_kwargs = {
            "from_user": {"read_only": True},
            "rejected": {"read_only": True},
            "viewed": {"read_only": True},
            "created": {"read_only": True}
        }

    def validate(self, attrs):
        from_user = self.context["request"].user
        to_user = attrs["to_user"]

        if not from_user.profile.username:
            raise serializers.ValidationError(_("Update your profile first"))

        if from_user == to_user:
            raise serializers.ValidationError(_(
                "You can't request yourself"
            ))

        if FriendshipRequest.objects.filter(
            from_user=from_user, to_user=to_user
        ).exists():
            raise serializers.ValidationError(_("Already Requested"))
        if FriendshipRequest.objects.filter(
            from_user=to_user, to_user=from_user
        ).exists():
            raise serializers.ValidationError(_("user already requested you"))

        if Friend.objects.filter(
            from_user=from_user, to_user=to_user
        ).exists():
            raise serializers.ValidationError(_(
                "you both are already friends"
            ))

        if Block.objects.filter(blocker=from_user, blocked=to_user):
            raise serializers.ValidationError(_("you blocked this user"))

        if Block.objects.filter(blocker=to_user, blocked=from_user):
            raise serializers.ValidationError(_("user blocked you"))

        if not Follow.objects.filter(follower=from_user, followee=to_user):
            Follow.objects.add_follower(from_user, to_user)

        return attrs

    def create(self, validated_data):
        from_user = self.context["request"].user
        return Friend.objects.add_friend(from_user, **validated_data)


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = (
            "id", "from_user", "to_user", "created"
        )
