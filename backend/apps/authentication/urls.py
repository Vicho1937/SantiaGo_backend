from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'authentication'

urlpatterns = [
    # Autenticación
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('me/', views.me_view, name='me'),
    path('google/', views.google_auth_view, name='google'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Perfil de usuario (accesibles desde /api/users/)
]

# Endpoints de perfil de usuario
user_urlpatterns = [
    path('profile/', views.update_profile_view, name='update_profile'),
    path('preferences/', views.update_preferences_view, name='update_preferences'),
    path('privacy/', views.update_privacy_view, name='update_privacy'),
    # NOTA: Avatar ahora se maneja en /api/media/profile/upload/ (Cloudinary)
]
