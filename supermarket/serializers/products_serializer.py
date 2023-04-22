from rest_framework import serializers

from ..models import Products


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = (
            "id",
            "product_name",
            "description",
            "images",
            "store",
            "product_type",
            "created",
            "updated"
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }
