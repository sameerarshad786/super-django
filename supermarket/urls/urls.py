from django.urls import path, include

from .product_urls import SCRAPED_PRODUCTS_URLS


urlpatterns = [
    path("outside-sources/", include(SCRAPED_PRODUCTS_URLS))
]
