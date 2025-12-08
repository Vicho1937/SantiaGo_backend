"""
URLs para gestión de media
"""
from django.urls import path
from . import views

app_name = 'media'

urlpatterns = [
    # Upload de foto de perfil
    path('profile/upload/', views.upload_profile_picture, name='upload_profile_picture'),
    path('profile/delete/', views.delete_profile_picture, name='delete_profile_picture'),

    # Upload de fotos de negocios
    path('business/<int:business_id>/upload/', views.upload_business_photo, name='upload_business_photo'),
]
