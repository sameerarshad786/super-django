from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from friendship.models import FriendshipRequest, Friend


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

    def to_representation(self, instance):
        request = self.context["request"]
        data = dict()
        data["id"] = instance.id
        data["user_id"] = instance.from_user.id
        data["username"] = instance.from_user.profile.username
        data["from_user"] = instance.from_user.email
        data["profile_image"] = request.build_absolute_uri(
            instance.from_user.profile.profile_image.url
        )
        data["viewed"] = instance.viewed
        data["send"] = instance.created
        return data

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
            raise serializers.ValidationError(_(
                "you both are already friends"
            ))

        return attrs

    def create(self, validated_data):
        from_user = self.context["request"].user
        return Friend.objects.add_friend(from_user, **validated_data)


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = (
            "id", "from_user", "to_user"
        )
