from rest_framework import generics

from products.models import Cart
from products.serializers import CartSerializer


class CartListAPIView(generics.ListAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class AddProductsAPIView(generics.CreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    lookup_field = "product_id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["product_id"] = self.kwargs.get("product_id")
        return context


class IncreaseOrDecreaseProductQuantityAPIView(generics.UpdateAPIView):
    serializer_class = CartSerializer
    lookup_field = "product_id"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class RemoveProductsAPIView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    lookup_field = "product_id"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
