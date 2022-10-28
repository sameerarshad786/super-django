from rest_framework import generics, parsers

from core.permissions import IsOwner
from post.serializers.remarks_serializer import (
    PostRemarkSerializer, CommentRemarksSerializer, CommentsSerializer
)
from post.models.remarks_model import PostRemarks, CommentRemarks, Comments


class PostRemarkCreateAPIView(generics.CreateAPIView):
    serializer_class = PostRemarkSerializer
    queryset = PostRemarks.objects.all()


class PostRemarkUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PostRemarkSerializer
    queryset = PostRemarks.objects.all()
    permission_classes = (IsOwner, )


class PostRemarkDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PostRemarkSerializer
    queryset = PostRemarks.objects.all()
    permission_classes = (IsOwner, )


class CommentRemarksCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentRemarksSerializer
    queryset = CommentRemarks.objects.all()


class CommentRemarksUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CommentRemarksSerializer
    queryset = CommentRemarks.objects.all()
    permission_classes = (IsOwner, )


class CommentRemarksDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CommentRemarksSerializer
    queryset = CommentRemarks.objects.all()
    permission_classes = (IsOwner, )


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()
    parser_classes = (parsers.MultiPartParser, )


class CommentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CommentsSerializer
    parser_classes = (parsers.MultiPartParser, )
    queryset = Comments.objects.all()
    permission_classes = (IsOwner, )


class CommentDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()
    permission_classes = (IsOwner, )
