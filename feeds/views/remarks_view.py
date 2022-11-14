from rest_framework import viewsets, parsers

from ..models import Remarks
from ..serializers import RemarkSerializer
from core.permissions import IsOwner


class RemarkViewSets(viewsets.ModelViewSet):
    serializer_class = RemarkSerializer
    queryset = Remarks.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )
