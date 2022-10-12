from rest_framework import generics, status
from rest_framework.response import Response

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


class PostRemarkDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PostRemarkSerializer
    queryset = PostRemark.objects.all()

    def destroy(self, request, *args, **kwargs):
        if PostRemark.objects.filter(user=request.user):
            return super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "403 forbidden"},
            status=status.HTTP_403_FORBIDDEN
        )


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()


class CommentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        return Comments.objects.filter(user=self.request.user)


class CommentDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        return Comments.objects.filter(user=self.request.user)
