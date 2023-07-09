from django.contrib import admin

from .models import (
    Products, ProductSource
)


class ProductSourceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "domain",
        "icon"
    )


class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "source",
        "name",
        "type",
        "image"
    )


admin.site.register(ProductSource, ProductSourceAdmin)
admin.site.register(Products, ProductsAdmin)
