from rest_framework import serializers

from products.models import ShippingAddress


class ShippingAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingAddress
        fields = (
            "id",
            "user",
            "country_code",
            "country",
            "city",
            "province",
            "street_address",
            "postal_code",
            "meta",
            "phone_number"
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        return ShippingAddress.objects.create(user=user, **validated_data)
