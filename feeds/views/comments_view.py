from rest_framework import viewsets, parsers

from ..models import Comments
from ..serializers import CommentSerializer
from core.permissions import IsOwner


class CommentViewSets(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )
