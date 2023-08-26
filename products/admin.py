from django.contrib import admin
from .models import Products, Cart


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "brand",
        "created",
        "updated"
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
