from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, exceptions

from post.models.remarks_model import PostRemarks, CommentRemarks, Comments


class PostRemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostRemarks
        fields = (
            "id", "user", "on_post", "popularity",
            "updated", "created"
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        popularity = validated_data.get("popularity")
        on_post = validated_data.get("on_post")
        remark = PostRemarks.objects.filter(
            user=user, on_post=on_post
        )

        if remark:
            if remark.filter(popularity=popularity).exists():
                raise exceptions.ValidationError(_("Entry already exists"))
            remark.delete()
            return PostRemarks.objects.create(user=user, **validated_data)
        return PostRemarks.objects.create(user=user, **validated_data)


class CommentRemarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentRemarks
        fields = (
            "id", "user", "on_post", "on_comment", "popularity",
            "updated", "created"
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        popularity = validated_data.get("popularity")
        on_post = validated_data.get("on_post")
        on_comment = validated_data.get("on_comment")
        remark = CommentRemarks.objects.filter(
            user=user, on_post=on_post, on_comment=on_comment
        )
        if remark:
            if remark.filter(popularity=popularity).exists():
                raise exceptions.ValidationError(_("Entry already exists"))
            remark.delete()
            return CommentRemarks.objects.create(user=user, **validated_data)
        return CommentRemarks.objects.create(user=user, **validated_data)


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = (
            "id", "user", "on_post", "parent", "comment", "files", "updated",
            "created"
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        return Comments.objects.create(user=user, **validated_data)
