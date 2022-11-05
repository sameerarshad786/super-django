from rest_framework import serializers

from friendship.models import Block


class BlockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ("blocker", "blocked", "created")
        extra_kwargs = {
            "blocker": {"read_only": True},
            "created": {"read_only": True}
        }

    def create(self, validated_data):
        blocker = self.context["request"].user
        return Block.objects.add_block(blocker, **validated_data)
