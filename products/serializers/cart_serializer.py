from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from products.models import Cart, Products
from profiles.serializers import UserSerializer
from products.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "user", "product", "quantity")

    def validate(self, attrs):
        product = self.context.get("product_id")
        user = self.context["request"].user
        if Cart.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError(_("product already added"))
        return attrs

    def create(self, validated_data):
        product_id = self.context.get("product_id")
        user = self.context["request"].user
        return Cart.objects.create(
            user=user, product=product_id, **validated_data
        )

    def get_product(self, obj):
        return ProductSerializer(
            Products.objects.get(id=obj.product)
        ).data
