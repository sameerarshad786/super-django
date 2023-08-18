from django_filters import rest_framework as filters

from .models.product_model import Products
from core.custom_filter_fields import DecimalRangeFilter


class ProductsFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    type = filters.CharFilter(field_name="type__type", lookup_expr="icontains")
    brand = filters.ChoiceFilter(choices=Products.Brand.choices)
    condition = filters.ChoiceFilter(choices=Products.Condition.choices)
    source = filters.ChoiceFilter(choices=Products.Source.choices)
    price = DecimalRangeFilter()

    class Meta:
        model = Products
        fields = ("name", "type", "condition", "price", "brand", "source")
