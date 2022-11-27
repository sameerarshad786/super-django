from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from friendship.models import Block, Friend, Follow, FriendshipRequest

from core.tasks.timesince_calculations import get_timesince


class BlockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ("blocker", "blocked", "created")
        extra_kwargs = {
            "blocker": {"read_only": True},
            "created": {"read_only": True}
        }

    def to_representation(self, instance):
        request = self.context["request"]
        data = dict()
        if instance.blocker == request.user:
            data["id"] = instance.id
            data["user_id"] = instance.blocked.id
            data["username"] = instance.blocked.profile.username
            data["email"] = instance.blocked.email
            data["profile_image"] = request.build_absolute_uri(
                instance.blocked.profile.profile_image.url
            )
            data["created"] = get_timesince(instance.created)
        return data

    def validate(self, attrs):
        blocker = self.context["request"].user
        blocked = attrs["blocked"]
        block_user = Block.objects.filter(blocker=blocker, blocked=blocked)

        if not blocker.profile.username:
            raise serializers.ValidationError(_("Update your profile first"))

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
