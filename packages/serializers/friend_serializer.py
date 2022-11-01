from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from friendship.models import FriendshipRequest, Friend


class SendFriendShipRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendshipRequest
        fields = (
            "id", "from_user", "to_user", "rejected", "viewed", "created"
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
            raise serializers.ValidationError(_("you both are already friends"))

        return attrs

    def create(self, validated_data):
        from_user = self.context["request"].user
        to_user = validated_data.get("to_user")
        return FriendshipRequest.objects.create(
            from_user=from_user, to_user=to_user
        )


class AcceptFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = (
            "id", "from_user", "to_user", "rejected", "viewed", "created"
        )
        extra_kwargs = {
            "from_user": {"read_only": True},
            "created": {"read_only": True}
        }
