from django.urls import path

from . import views


urlpatterns = [
    path("products/", views.SupermarketProductAPIView.as_view(), name="products")
]
