from django.utils import timezone

from rest_framework import serializers

from ..models import Stores, StoreTypes


class StoreSerializer(serializers.ModelSerializer):
    store_type = serializers.CharField(
        max_length=150, source="store_type.type")

    class Meta:
        model = Stores
        fields = (
            "id",
            "user",
            "store_name",
            "store_type",
            "images",
            "is_verified",
            "location",
            "created",
            "updated"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "is_verified": {"read_only": True}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        type = validated_data.get("store_type")["type"].capitalize()
        store_name = validated_data.get("store_name")
        images = validated_data.get("images")
        location = validated_data.get("location")
        try:
            store_type = StoreTypes.objects.get(type=type)
        except StoreTypes.DoesNotExist:
            store_type = StoreTypes.objects.create(type=type)

        store = Stores(
            user=user,
            store_type=store_type,
            store_name=store_name,
            images=images,
            location=location,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        store.save()
        return store

    def update(self, instance, validated_data):
        type = validated_data.get("store_type")["type"].capitalize()
        store_name = validated_data.get("store_name")
        images = validated_data.get("images")
        location = validated_data.get("location")
        try:
            store_type = StoreTypes.objects.get(type=type)
        except StoreTypes.DoesNotExist:
            store_type = StoreTypes.objects.create(type=type)

        instance.store_type = store_type
        instance.store_name = store_name
        instance.images = images
        instance.location = location
        instance.save()
        return instance
