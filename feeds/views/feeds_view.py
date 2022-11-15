from rest_framework import parsers, generics

from ..models import Feeds
from ..serializers import FeedSerializer
from core.permissions import IsOwner


class FeedsAPIView(generics.ListAPIView):
    serializer_class = FeedSerializer
    queryset = Feeds.objects.all()


class FeedsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = FeedSerializer
    queryset = Feeds.objects.all()
    parser_classes = (parsers.MultiPartParser, )


class FeedsCreateAPIView(generics.CreateAPIView):
    serializer_class = FeedSerializer
    queryset = Feeds.objects.all()
    parser_classes = (parsers.MultiPartParser, )


class FeedsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = FeedSerializer
    queryset = Feeds.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )


class FeedsDeleteAPIView(generics.DestroyAPIView):
    serializer_class = FeedSerializer
    queryset = Feeds.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )
