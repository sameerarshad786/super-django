from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from friendship.models import Friend, FriendshipRequest, AlreadyFriendsError


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ("id", "from_user", "to_user", "created")
        extra_kwargs = {
            "from_user": {"read_only": True},
            "created": {"read_only": True}
        }

    def validate(self, attrs):
        from_user = self.context["request"].user
        to_user = attrs["to_user"]

        alread_requested = FriendshipRequest.objects.filter(
            from_user=from_user, to_user=to_user
        )
        if alread_requested.exists():
            raise serializers.ValidationError(_("already requested"))

        return attrs

    def create(self, validated_data):
        from_user = self.context["request"].user
        to_user = validated_data.get("to_user")
        try:
            return FriendshipRequest.objects.create(
                from_user=from_user, to_user=to_user
            )
        except AlreadyFriendsError:
            raise serializers.ValidationError(_("already friend"))


class FriendShipRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendshipRequest
        fields = (
            "id", "from_user", "to_user", "rejected", "viewed", "created"
        )
        extra_kwargs = {
            "from_user": {"read_only": True},
            "requested": {"read_only": True}
        }

    def create(self, validated_data):
        to_user = self.context["request"].user
        friend_request = FriendshipRequest.objects.get(to_user=to_user)
        friend_request.accept()
        return super().create(validated_data)
