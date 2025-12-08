"""
URLs para el asistente AI
"""
from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
    path('suggest-route/', views.suggest_route_view, name='suggest_route'),
    path('health/', views.health_check_view, name='health_check'),
]
