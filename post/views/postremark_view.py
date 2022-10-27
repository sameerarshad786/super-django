from rest_framework import generics, parsers

from core.permissions import IsOwner
from post.serializers.postremark_serializer import (PostRemarkSerializer,
                                                    CommentsSerializer)
from post.models.postremark_model import PostRemark, Comments


class PostRemarkCreateAPIView(generics.CreateAPIView):
    serializer_class = PostRemarkSerializer
    queryset = PostRemark.objects.all()


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


class CommentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CommentsSerializer
    parser_classes = (parsers.MultiPartParser,)
    queryset = Comments.objects.all()
    permission_classes = (IsOwner, )


class CommentDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()
    permission_classes = (IsOwner, )
