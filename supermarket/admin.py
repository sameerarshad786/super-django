from django.contrib import admin

from .models import (
    Products, ProductSource, ProductTypes
)


class ProductTypesAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "valid_name")


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
        "type_id",
        "image"
    )


admin.site.register(ProductTypes, ProductTypesAdmin)
admin.site.register(ProductSource, ProductSourceAdmin)
admin.site.register(Products, ProductsAdmin)
