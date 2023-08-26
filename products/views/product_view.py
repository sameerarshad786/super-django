from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics

from products.models import Products
from products.serializers import ProductSerializer, RetrieveProductsSerializer
from products.filters import ProductsFilter
from core.pagination import StandardResultsSetPagination


class ProductsListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Products.objects.all().using("supermarket")
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductsFilter

    def get_queryset(self):
        if self.request.GET:
            return super().get_queryset()
        else:
            return super().get_queryset().order_by("?")


class RetrieveProductAPIView(generics.RetrieveAPIView):
    serializer_class = RetrieveProductsSerializer
    queryset = Products.objects.all().using("supermarket")
