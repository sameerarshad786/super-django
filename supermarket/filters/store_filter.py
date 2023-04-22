from django_filters import rest_framework as filters
from ..models import Stores


class StoreFilter(filters.FilterSet):
    store_name = filters.CharFilter(
        field_name="name", lookup_expr="icontains")
    store_type = filters.CharFilter(
        field_name="type__type", lookup_expr="icontains")

    class Meta:
        model = Stores
        fields = ("store_name", "store_type")
