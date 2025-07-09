from django.urls import path
from .views import AIChatView, TextToSpeechView

urlpatterns = [
    path('chat/', AIChatView.as_view(), name='chat'),
    path('tts/', TextToSpeechView.as_view(), name='tts'),
]