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

    # Upload de fotos de negocios (temporal para creación)
    path('business/upload/', views.upload_business_photo_temp, name='upload_business_photo_temp'),
    
    # Upload de fotos de negocios (para negocios existentes)
    path('business/<uuid:business_id>/upload/', views.upload_business_photo, name='upload_business_photo'),
]
