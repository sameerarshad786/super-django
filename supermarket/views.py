import os
import requests

from django.http import JsonResponse

from rest_framework import views, status


class SupermarketProductAPIView(views.APIView):
    
    def get(self, request, *args, **kwargs):
        name = request.GET.get("name", "")
        type = request.GET.get("type", "")
        condition = request.GET.get("condition", "")
        price = request.GET.get("price", "")
        brand = request.GET.get("brand", "")
        source = request.GET.get("source", "")
        page = request.GET.get("page", 1)
        page_size = request.GET.get("page", 10)
        query_params = f"name={name}&type={type}&condition={condition}&price={price}&brand={brand}&source={source}&page={page}&page_size={page_size}" # noqa
        source_url = os.getenv("SUPERMARKET")
        products = requests.get(f"{source_url}?{query_params}")
        return JsonResponse(products.json(), status=status.HTTP_200_OK)
