import threading

from rest_framework import serializers

from finance.models import ProductCheckout
from finance.service import buy_product


class ProductCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCheckout
        fields = ("id", "user", "product", "discounted", "pay_through")
        extra_kwargs = {
            "user": {"read_only": True},
            "product": {"read_only": True}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        product = self.context["product"]
        threading.Thread(buy_product(user, product))
        return validated_data
