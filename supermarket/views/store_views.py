from rest_framework import generics, parsers

from ..models import Store
from ..serializers import StoreSerializer
from core.permissions import IsOwner


class StoreRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    lookup_field = "name"

    def get_queryset(self):
        store = Store.objects.filter(name=self.kwargs["name"])
        return store


class StoreCreateAPIView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    parser_classes = (parsers.MultiPartParser, )


class StoreUpdateAPIView(generics.UpdateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )
