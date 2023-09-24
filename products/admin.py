from django.contrib import admin
from .models import Products, ProductTypes, Cart, ShippingAddress


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_name",
        "brand",
        "source",
        "created",
        "updated"
    )


@admin.register(ProductTypes)
class ProductTypesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "valid_name"
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "quantity",
        "created",
        "updated"
    )


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "country",
        "city"
    )
