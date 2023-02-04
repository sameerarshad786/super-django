from django.shortcuts import render


def chatbot(request):
    context = {"title": "chatbot"}
    return render(request, "dialogflow/chat.html", context=context)
