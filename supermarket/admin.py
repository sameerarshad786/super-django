from django.contrib import admin

from .models import StoreTypes, Stores, Products, ProductTypes


class StoreTypesAdmin(admin.ModelAdmin):
    list_display = (
        "id", "type", "valid_name", "created", "updated"
    )


admin.site.register(StoreTypes, StoreTypesAdmin)


class StoreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "store_type",
        "store_name",
        "is_verified",
        "get_image",
        "created",
        "updated"
    )


admin.site.register(Stores, StoreAdmin)


class ProductTypesAdmin(admin.ModelAdmin):
    list_display = (
        "id", "type", "valid_name", "created", "updated"
    )


admin.site.register(ProductTypes, ProductTypesAdmin)


class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_name",
        "description",
        "images",
        "store",
        "product_type",
        "created",
        "updated"
    )


admin.site.register(Products, ProductsAdmin)
