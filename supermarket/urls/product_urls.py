from django.urls import path
from ..views import product_views


SCRAPED_PRODUCTS_URLS = [
    path("products/", product_views.ProductsAPIView.as_view(), name="products"),
]
