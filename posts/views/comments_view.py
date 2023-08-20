from rest_framework import parsers, generics, status
from rest_framework.response import Response

from ..models import Comments
from ..serializers import CommentSerializer
from ..service import comment_popularities, user_replied, total_replies


class CommentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.filter(
            post=self.kwargs["post_id"], parent=None).order_by("-created_at")

    def get(self, request, *args, **kwargs):
        query = self.filter_queryset(self.get_queryset())
        query = comment_popularities(query, request.user)
        query = user_replied(query, request.user)
        query = total_replies(query)
        serializer = self.get_serializer(
            query, context={"request": request}, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)


class ChildCommentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        id = self.kwargs["id"]
        return Comments.objects.filter(
            id=id,
            post_id=post_id
        )

    def get(self, request, *args, **kwargs):
        query = self.filter_queryset(self.get_queryset())
        query = comment_popularities(query, request.user)
        query = user_replied(query, request.user)
        query = total_replies(query)
        serializer = self.get_serializer(
            query, context={"request": request}, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)


class CommentsCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    parser_classes = (parsers.MultiPartParser, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["post_id"] = self.kwargs.get("post_id")
        return context


class CommentsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CommentSerializer
    parser_classes = (parsers.MultiPartParser, )
    lookup_field = "id"

    def get_queryset(self):
        return Comments.objects.filter(user=self.request.user)


class CommentsDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Comments.objects.filter(user=self.request.user)
