from django.urls import path
from message import views
from .dialogflow_webhook import webhook


urlpatterns = [
    path('chatbot/', views.MessageBotAPIView.as_view(), name='chatbot'),
    path('webhook/', webhook, name='dailogflow-webhook')
]
