from rest_framework import generics, status
from rest_framework.response import Response

from products.models import ShippingAddress
from products.serializers import ShippingAddressSerializer


class ShippingAddressAPIView(generics.GenericAPIView):
    serializer_class = ShippingAddressSerializer

    def get_object(self):
        return ShippingAddress.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            self.get_object(), context={"request": request}
        ).data
        return Response(serializer, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            self.get_object(),
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
