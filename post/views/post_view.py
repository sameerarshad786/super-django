from rest_framework import generics, parsers

from core.permissions import IsOwner
from post.serializers.post_serializer import PostSerializer
from post.models.post_model import Post


class PostAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = (parsers.MultiPartParser, )


class PostUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )


class PostDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )
