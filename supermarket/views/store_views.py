from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, parsers, permissions
from rest_framework import throttling

from ..models import Stores
from ..serializers import StoreSerializer
from ..filters import StoreFilter
from core.permissions import IsOwner


class StoreListAPIView(generics.ListAPIView):
    serializer_class = StoreSerializer
    queryset = Stores.objects.all()
    permission_classes = (permissions.AllowAny, )
    throttle_classes = (throttling.AnonRateThrottle, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = StoreFilter


class StoreRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = StoreSerializer
    queryset = Stores.objects.all()
    permission_classes = (permissions.AllowAny, )
    throttle_classes = (throttling.AnonRateThrottle, )
    lookup_field = "name"


class StoreCreateAPIView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    queryset = Stores.objects.all()
    parser_classes = (parsers.MultiPartParser, )


class StoreUpdateAPIView(generics.UpdateAPIView):
    serializer_class = StoreSerializer
    queryset = Stores.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )


class StoreDestroyAPIView(generics.DestroyAPIView):
    serializer_class = StoreSerializer
    queryset = Stores.objects.all()
    permission_classes = (IsOwner, )
