from django.http import JsonResponse

from rest_framework import views

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.cloud import dialogflow_v2 as dialogflow

from .serializers import BotMessageSerializer
from .models.bot_keyerrors_models import BotKeyErrors



class MessageBotAPIView(views.APIView):
    text_param_config = openapi.Parameter(
        "text",
        in_=openapi.IN_QUERY,
        description="text for dialogflow",
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[text_param_config])
    def get(self, request, *args, **kwargs):
        text = self.request.GET.get("text")
        session_client = dialogflow.SessionsClient()
        session_id = request.session.session_key
        session = session_client.session_path("newagent-qscn", session_id)
        text_input = dialogflow.types.TextInput(
            text=text,
            language_code='en-US'
        )
        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session,
            query_input=query_input
        )
        data = {
            'Bot': f'{response.query_result.fulfillment_text}'
        }
        return JsonResponse(data, safe=False, status=200)
