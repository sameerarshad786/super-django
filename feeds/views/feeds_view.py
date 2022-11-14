from rest_framework import viewsets, parsers

from ..models import Feeds
from ..serializers import FeedSerializer
from core.permissions import IsOwner


class FeedViewSets(viewsets.ModelViewSet):
    serializer_class = FeedSerializer
    queryset = Feeds.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )
