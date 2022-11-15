from rest_framework import parsers, generics

from ..models import Comments
from ..serializers import CommentSerializer
from core.permissions import IsOwner


class CommentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    parser_classes = (parsers.MultiPartParser, )


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
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )
