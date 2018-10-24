from django.shortcuts import render
from .chatbot import get_response
from django.http import JsonResponse

# Create your views here.
def chat(request):
    context = {}
    return render(request, 'chat.html', context)

def ajax_chat(request):
    message = request.GET.get('message', None)
    chat_response = get_response(message)
    data = {
        'bot_respnse': chat_response
    }
    return JsonResponse(data)

