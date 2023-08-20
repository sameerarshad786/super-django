from rest_framework import generics, status
from rest_framework.response import Response

from ..models import Remarks
from ..serializers import RemarkSerializer


class PostRemarksRetrieveAPIView(generics.ListAPIView):
    serializer_class = RemarkSerializer

    def get_queryset(self):
        return Remarks.objects.filter(
            post_id=self.kwargs["post_id"], comment=None)


class CommentRemarksRetrieveAPIView(generics.ListAPIView):
    serializer_class = RemarkSerializer

    def get_queryset(self):
        return Remarks.objects.filter(
            post=self.kwargs["post_id"],
            comment=self.kwargs["comment_id"]
        )


class RemarksCreateAPIView(generics.CreateAPIView):
    serializer_class = RemarkSerializer
    queryset = Remarks.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["post_id"] = self.kwargs.get("post_id")
        return context


class RemarksUpdateAPIView(generics.GenericAPIView):
    serializer_class = RemarkSerializer

    def get_object(self):
        return Remarks.objects.get(
            post=self.kwargs["post_id"], user=self.request.user)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            instance=self.get_object(),
            context={"request": request, "post_id": kwargs["post_id"]}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RemarksDeleteAPIView(generics.GenericAPIView):
    serializer_class = RemarkSerializer

    def get_object(self):
        return Remarks.objects.get(
            post_id=self.kwargs["post_id"], user=self.request.user
        )

    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
        except Remarks.DoesNotExist:
            return Response(
                {"error": "instance does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
