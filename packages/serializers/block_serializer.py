from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from friendship.models import Block, Friend, Follow, FriendshipRequest


class BlockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ("blocker", "blocked", "created")
        extra_kwargs = {
            "blocker": {"read_only": True},
            "created": {"read_only": True}
        }

    def validate(self, attrs):
        blocker = self.context["request"].user
        blocked = attrs["blocked"]
        block_user = Block.objects.filter(blocker=blocker, blocked=blocked)

        if blocker == blocked:
            raise serializers.ValidationError(_(
                "You can't block your self"
            ))

        if block_user.exists():
            raise serializers.ValidationError(_(
                "You already block this user"
            ))

        if Friend.objects.are_friends(blocker, blocked):
            Friend.objects.remove_friend(blocker, blocked)

        if Follow.objects.follows(blocker, blocked):
            Follow.objects.remove_follower(blocker, blocked)

        if Follow.objects.follows(blocked, blocker):
            Follow.objects.remove_follower(blocked, blocker)

        if Friend.objects.requests(blocked):
            FriendshipRequest.objects.filter(
                from_user=blocker, to_user=blocked
            ).delete()

        if Friend.objects.requests(blocker):
            FriendshipRequest.objects.filter(
                from_user=blocked, to_user=blocker
            ).delete()

        return attrs

    def create(self, validated_data):
        blocker = self.context["request"].user
        return Block.objects.add_block(blocker, **validated_data)
