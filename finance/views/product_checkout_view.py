from rest_framework import generics, status
from rest_framework.response import Response

from finance.serializers import ProductCheckoutSerializer
from products.models import Products


class ProductCheckoutCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductCheckoutSerializer
    queryset = Products.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request, "product": self.get_object()}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "this will takes upto 3-5 minutes, we will inform you after checkout"}, # noqa
            status=status.HTTP_200_OK
        )
