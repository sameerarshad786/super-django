from rest_framework import generics, status
from rest_framework.response import Response

from ..serializers import UserSensitiveInformationSerializer
from ..models import UserSensitiveInformation


class UserSensitiveInformationAPIView(generics.GenericAPIView):
    serializer_class = UserSensitiveInformationSerializer

    def get_object(self):
        return UserSensitiveInformation.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=self.get_object(), context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwagrs):
        serializer = self.serializer_class(
            data=request.data,
            instance=self.get_object(),
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
