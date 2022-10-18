from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, exceptions

from post.models.postremark_model import PostRemark, Comments


class PostRemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostRemark
        fields = ("id", "user", "on_post", "popularity", "updated", "created")
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def create(self, validated_data):
        on_post = validated_data.get("on_post")
        user = self.context["request"].user
        if PostRemark.objects.filter(user=user, on_post=on_post).exists():
            raise exceptions.NotAcceptable(_("Entry already created"))
        return PostRemark.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user == instance.user:
            return super().update(instance, validated_data)
        raise exceptions.PermissionDenied(_(
            "403 forbidden"
        ))


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = (
            "id", "user", "on_post", "comment", "files", "updated", "created"
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        return Comments.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user == instance.user:
            return super().update(instance, validated_data)
        raise exceptions.PermissionDenied(_(
            "403 forbidden"
        ))
