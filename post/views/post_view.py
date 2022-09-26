from rest_framework import generics, parsers, status
from rest_framework.response import Response

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
        if Post.objects.filter(user=request.user):
            return super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "403 forbidden"}, status=status.HTTP_403_FORBIDDEN
        )
