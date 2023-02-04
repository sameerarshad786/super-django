from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..models import Store, Types


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = (
            "id",
            "user",
            "name",
            "store_type",
            "image",
            "is_verified",
            "location"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "is_verified": {"required": False, "read_only": True},
            "type": {"read_only": True},
            "location": {"required": True}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        store_type = validated_data.get("store_type")
        if Types.objects.filter(type=store_type):
            type_st = Types.objects.get(type=store_type)
            return Store.objects.create(
                user=user, type=type_st, **validated_data
            )
        type = Types.objects.create(type=store_type)
        return Store.objects.create(
            user=user, type=type, **validated_data
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["created"] = instance.created()
        representation["updated"] = instance.updated()
        return representation
