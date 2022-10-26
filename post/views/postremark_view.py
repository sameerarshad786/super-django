from rest_framework import generics, status, parsers
from rest_framework.response import Response

from core.permissions import IsOwner
from post.serializers.postremark_serializer import (PostRemarkSerializer,
                                                    CommentsSerializer)
from post.models.postremark_model import PostRemark, Comments


class PostRemarkCreateAPIView(generics.CreateAPIView):
    serializer_class = PostRemarkSerializer
    queryset = PostRemark.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostRemarkUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PostRemarkSerializer
    queryset = PostRemark.objects.all()
    permission_classes = (IsOwner, )


class PostRemarkDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PostRemarkSerializer
    queryset = PostRemark.objects.all()
    permission_classes = (IsOwner, )


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()
    parser_classes = (parsers.MultiPartParser,)


class CommentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()
    parser_classes = (parsers.MultiPartParser,)

    def get(self, request, *args, **kwargs):
        result = []
        for comment in Comments.objects.filter(id=kwargs["pk"]):
            result.append({
                "id": comment.id,
                "user": str(comment.user),
                "username": comment.user.profile.username,
                "profile_image": request.build_absolute_uri(
                    comment.user.profile.profile_image.url
                ),
                "comment": comment.comment,
                "created": comment.created(),
                "updated": comment.updated(),
                "files": request.build_absolute_uri(
                    comment.files.url) if comment.files else None,
                "child_id": str(comment.parent),
                "child": str(Comments.get_replies(comment))
            })
        return Response(result)


class CommentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CommentsSerializer
    parser_classes = (parsers.MultiPartParser,)
    queryset = Comments.objects.all()
    permission_classes = (IsOwner, )


class CommentDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()
    permission_classes = (IsOwner, )
