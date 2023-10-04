from rest_framework import serializers

from ..models.product_model import Products, ProductTypes
from core.custom_serializer_fields import DecimalRangeFieldSerializer


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypes
        fields = ("id", "type")


class ProductSerializer(serializers.ModelSerializer):
    # price = DecimalRangeFieldSerializer()

    class Meta:
        model = Products
        fields = (
            "id",
            "name",
            "image",
            # "price",
            "brand",
            "condition",
            "ratings",
            "source",
            "url"
        )


class RetrieveProductsSerializer(serializers.ModelSerializer):
    price = DecimalRangeFieldSerializer()
    type = ProductTypeSerializer()

    class Meta:
        model = Products
        fields = (
            "id",
            "name",
            "description",
            "type",
            "brand",
            "image",
            "original_price",
            "price",
            "condition",
            "items_sold",
            "shipping_charges",
            "ratings",
            "discount",
            "source",
            "url"
        )
