from rest_framework import serializers

from products.models import Cart
from profiles.serializers import UserSerializer
from products.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "user", "product", "quantity")

    def create(self, validated_data):
        product_id = self.context.get("view").kwargs.get("product_id")
        user = self.context["request"].user
        return Cart.objects.create(
            user=user, product_id=product_id, **validated_data)
