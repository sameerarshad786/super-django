from django.http import JsonResponse
from rest_framework import status


def not_found(request, exception):
    data = {
        'error': 'Not Found (404)'
    }
    return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
