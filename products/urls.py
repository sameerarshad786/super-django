from django.urls import path, include

from . import views


PRODUCTS_PATTERNS = [
    path("list/", views.ProductsListAPIView.as_view(), name="products-list"),
    path(
        "retrieve/<uuid:pk>/",
        views.RetrieveProductAPIView.as_view(),
        name="product-details"
    )
]

CART_PATTERNS = [
    path("list/", views.CartListAPIView.as_view(), name="cart-list"),
    path(
        "add-products/<uuid:product_id>/",
        views.AddProductsAPIView.as_view(),
        name="add-products"
    ),
    path(
        "increase-or-decrease/<uuid:product_id>",
        views.IncreaseOrDecreaseProductQuantityAPIView.as_view(),
        name="increase-or-decrease"
    ),
    path(
        "remove-products/<uuid:product_id>/",
        views.RemoveProductsAPIView.as_view(),
        name="remove-products"
    )
]

SHIPPING_ADDRESS_PATTERN = [
    path(
        "get/",
        views.ShippingAddressAPIView.as_view(),
        name="shipping-address"
    )
]


urlpatterns = [
    path("products/", include(PRODUCTS_PATTERNS)),
    path("cart/", include(CART_PATTERNS)),
    path("shipping-address/", include(SHIPPING_ADDRESS_PATTERN))
]
