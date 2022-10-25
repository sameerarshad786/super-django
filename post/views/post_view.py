from rest_framework import generics, parsers

from core.permissions import IsOwner
from post.serializers.post_serializer import PostSerializer
from post.models.post_model import Post
from post.models.postremark_model import Comments, PostRemark


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        for post in Post.objects.all():
            if Comments.objects.filter(on_post=post.id):
                if PostRemark.objects.filter(
                    on_post=post.id, popularity="like"
                ):
                    return Post.objects.order_by(
                        "-postremark", "-comments", "-updated_at"
                    )
            return Post.objects.order_by("-created_at")


class PostCreateAPIView(generics.CreateAPIView):
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
    permission_classes = (IsOwner, )
