from rest_framework import generics

from ..models import Remarks
from ..serializers import RemarkSerializer
from core.permissions import IsOwner


class RemarksCreateAPIView(generics.CreateAPIView):
    serializer_class = RemarkSerializer
    queryset = Remarks.objects.all()


class RemarksUpdateAPIView(generics.UpdateAPIView):
    serializer_class = RemarkSerializer
    queryset = Remarks.objects.all()
    permission_classes = (IsOwner, )


class RemarksDeleteAPIView(generics.DestroyAPIView):
    serializer_class = RemarkSerializer
    queryset = Remarks.objects.all()
    permission_classes = (IsOwner, )
