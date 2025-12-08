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
from apps.authentication.urls import user_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include(user_urlpatterns)),  # User profile endpoints
    path('api/ai/', include('apps.ai_assistant.urls')),  # AI Assistant - RutaGO chatbot
    path('api/businesses/', include('apps.businesses.urls')),  # Includes categories endpoint
    path('api/routes/', include('apps.routes.urls')),
    path('api/', include('apps.reviews.urls')),  # Reviews endpoints include business_id in path
    path('api/media/', include('apps.media.urls')),  # Media uploads (Cloudinary)
]
