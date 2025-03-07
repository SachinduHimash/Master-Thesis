from django.urls import path
from .views import get_convo,get_values,chat_agent

urlpatterns = [
    path('convo/',get_convo,name='get_convos'),
    path('convo/get_values/',get_values,name='get_values'),
    path('convo/chat_agent/',chat_agent,name = "chat_agent")
]
