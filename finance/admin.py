from django.contrib import admin

from finance.models import ProductCheckout


@admin.register(ProductCheckout)
class ProductCheckoutAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "product", "discounted", "pay_through", "created"
    )
