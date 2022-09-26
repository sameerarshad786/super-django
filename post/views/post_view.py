from rest_framework import generics, parsers

from post.serializers.post_serializer import PostSerializer
from post.models.post_model import Post


class PostAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = (parsers.MultiPartParser,)


class PostUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = (parsers.MultiPartParser,)
    lookup_field = "pk"


class PostDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = (parsers.MultiPartParser,)
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
