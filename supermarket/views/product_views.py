from django_filters.rest_framework import DjangoFilterBackend

from ..models import Products
from ..serializers import ProductsSerializer
from ..filters import ProductsFilter
from core.pagination import StandardResultsSetPagination

from rest_framework import generics, permissions


class ProductsAPIView(generics.ListAPIView):
    serializer_class = ProductsSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Products.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductsFilter

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
