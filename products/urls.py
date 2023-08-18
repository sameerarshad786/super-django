from django.urls import path

from . import views


urlpatterns = [
    path("list/", views.ProductsListAPIView.as_view(), name="products")
]
