from decimal import Decimal

from django.db.models import F

from django_filters import rest_framework as filters

from ..models import Products


class DecimalRangeFilter(filters.BaseRangeFilter):
    def filter(self, qs, value):
        if value:
            if Decimal(value[0]) > 0 and Decimal(value[1]) > 0:
                return qs.filter(
                    price__lower__range=[Decimal(value[0]), F("price__upper")],
                    price__upper__range=[F("price__lower"), Decimal(value[1])]
                )
            elif Decimal(value[0]) > 0 and Decimal(value[1]) == 0:
                return qs.filter(
                    price__upper__lte=Decimal(value[0])
                )
            elif Decimal(value[0]) == 0 and Decimal(value[1]) > 0:
                return qs.filter(
                    price__lower__lte=Decimal(value[1])
                )
        return qs


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
