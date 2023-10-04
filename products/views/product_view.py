import json

from django_filters.rest_framework import DjangoFilterBackend
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import generics, permissions
from rest_framework.response import Response

from utils.elasticsearch import search_product_using_es

from products.models import Products
from products.serializers import ProductSerializer, RetrieveProductsSerializer
from products.filters import ProductsFilter
from core.pagination import StandardResultsSetPagination


class ProductsListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.AllowAny, )
    # filter_backends = (DjangoFilterBackend, )
    # filterset_class = ProductsFilter

    def get_queryset(self):
        response = search_product_using_es(
            "product_index",
            self.request.GET.get("name"),
            page=self.request.GET.get("page", 1),
            size=self.request.GET.get("page_size", 10)
        )
        data = list(map(lambda x:x['_source'], response['hits']['hits']))
        print(response.__dict__)
        return data


class RetrieveProductAPIView(generics.RetrieveAPIView):
    serializer_class = RetrieveProductsSerializer
    queryset = Products.objects.all()
