from django.urls import path

from finance import views


urlpatterns = [
    path(
        "product-checkout/<uuid:pk>/",
        views.ProductCheckoutCreateAPIView.as_view(),
        name="product-checkout"
    )
]
