from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from friendship.models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("follower", "followee", "created")
        extra_kwargs = {
            "follower": {"read_only": True},
            "created": {"read_only": True}
        }

    def validate(self, attrs):
        follower = self.context["request"].user
        followee = attrs["followee"]

        if Follow.objects.filter(
            follower=follower, followee=followee
        ).exists():
            raise serializers.ValidationError(_("already followed"))

        if follower == followee:
            raise serializers.ValidationError(_("You can't follow your self"))

        return attrs

    def create(self, validated_data):
        follower = self.context["request"].user
        return Follow.objects.add_follower(
            follower, **validated_data
        )
