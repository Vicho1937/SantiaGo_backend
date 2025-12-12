"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from apps.authentication.urls import user_urlpatterns


def api_root(request):
    """API root endpoint - muestra endpoints disponibles"""
    return JsonResponse({
        'message': 'Ruta Local API',
        'version': '1.0',
        'endpoints': {
            'auth': {
                'login': '/api/auth/login/',
                'register': '/api/auth/register/',
                'logout': '/api/auth/logout/',
                'me': '/api/auth/me/',
                'refresh': '/api/auth/refresh/',
                'google': '/api/auth/google/',
            },
            'users': {
                'profile': '/api/users/profile/',
                'preferences': '/api/users/preferences/',
                'privacy': '/api/users/privacy/',
            },
            'businesses': '/api/businesses/',
            'routes': '/api/routes/',
            'ai': '/api/ai/',
            'media': '/api/media/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),

    # DRF Browsable API Login (para la interfaz web de DRF)
    path('api-auth/', include('rest_framework.urls')),

    # API root
    path('api/', api_root, name='api-root'),

    # API endpoints
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include(user_urlpatterns)),  # User profile endpoints
    path('api/ai/', include('apps.ai_assistant.urls')),  # AI Assistant - RutaGO chatbot
    path('api/businesses/', include('apps.businesses.urls')),  # Includes categories endpoint
    path('api/routes/', include('apps.routes.urls')),
    path('api/reviews/', include('apps.reviews.urls')),  # Reviews endpoints
    path('api/media/', include('apps.media.urls')),  # Media uploads (Cloudinary)
]
