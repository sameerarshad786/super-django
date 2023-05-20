from rest_framework import serializers


class BotMessageSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)

    class Meta:
        fields = ("text", )
