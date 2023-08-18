from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics

from products.models import Products
from products.serializers import ProductsSerializer
from core.pagination import StandardResultsSetPagination
from .filters import ProductsFilter


class ProductsListAPIView(generics.ListAPIView):
    serializer_class = ProductsSerializer
    queryset = Products.objects.using("supermarket").all().order_by("?")
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductsFilter
