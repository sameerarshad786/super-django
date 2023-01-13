from rest_framework import parsers, generics, status
from rest_framework.response import Response

from ..models import Comments
from ..serializers import CommentSerializer
from core.permissions import IsOwner
from ..service import comment_popularities, user_replied, total_replies


class CommentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.filter(comment=None)

    def get(self, request, *args, **kwargs):
        query = self.filter_queryset(self.get_queryset())
        query = comment_popularities(query, request)
        query = user_replied(query, request)
        query = total_replies(query)
        serializer = self.get_serializer(
            query, context={"request": request}, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)


class ChildCommentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()

    def get(self, request, *args, **kwargs):
        query = Comments.objects.filter(id=kwargs["pk"])
        query = comment_popularities(query, request)
        query = user_replied(query, request)
        query = total_replies(query)
        serializer = self.get_serializer(
            query, context={"request": request}, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)


class CommentsCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    parser_classes = (parsers.MultiPartParser, )


class CommentsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )


class CommentsDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    permission_classes = (IsOwner, )
