from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, GoogleAuthSerializer


def get_tokens_for_user(user):
    """Genera tokens JWT para un usuario"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Registro de nuevo usuario"""
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'accessToken': tokens['access'],
                'refreshToken': tokens['refresh'],
                'tokenType': 'Bearer',
                'expiresIn': 900
            }
        }, status=status.HTTP_201_CREATED)

    return Response({
        'success': False,
        'errors': serializer.errors,
        'message': 'Error en la validación'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login con email y contraseña"""
    serializer = LoginSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        user = serializer.validated_data['user']
        user.last_login_at = timezone.now()
        user.save(update_fields=['last_login_at'])

        tokens = get_tokens_for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'accessToken': tokens['access'],
                'refreshToken': tokens['refresh'],
                'tokenType': 'Bearer',
                'expiresIn': 900
            }
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'errors': serializer.errors,
        'message': 'Credenciales inválidas'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout (invalidar token)"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'success': True,
            'message': 'Sesión cerrada exitosamente'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error al cerrar sesión'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """Obtener usuario actual"""
    return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth_view(request):
    """Login con Google OAuth"""
    serializer = GoogleAuthSerializer(data=request.data)

    if serializer.is_valid():
        # TODO: Implementar validación con Google OAuth
        return Response({
            'success': False,
            'message': 'Autenticación con Google no implementada aún'
        }, status=status.HTTP_501_NOT_IMPLEMENTED)

    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """Actualizar perfil del usuario"""
    user = request.user

    # Actualizar campos permitidos
    if 'first_name' in request.data:
        user.first_name = request.data['first_name']
    if 'last_name' in request.data:
        user.last_name = request.data['last_name']
    if 'phone' in request.data:
        user.phone = request.data['phone']
    if 'bio' in request.data:
        user.bio = request.data['bio']

    # Actualizar ubicación
    if 'location' in request.data:
        location = request.data['location']
        if isinstance(location, dict):
            user.location_city = location.get('city', '')
            user.location_state = location.get('state', '')
            user.location_country = location.get('country', 'Chile')

    user.save()

    return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_preferences_view(request):
    """Actualizar preferencias del usuario"""
    user = request.user

    if 'theme' in request.data:
        user.theme_preference = request.data['theme']
    if 'language' in request.data:
        user.preferred_language = request.data['language']
    if 'notifications' in request.data:
        notifications = request.data['notifications']
        if isinstance(notifications, dict):
            # Si cualquier notificación está habilitada, activar notifications_enabled
            user.notifications_enabled = any(notifications.values())

    user.save()

    return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_privacy_view(request):
    """Actualizar configuración de privacidad"""
    user = request.user

    if 'profileVisibility' in request.data:
        user.profile_visibility = request.data['profileVisibility']
    if 'showEmail' in request.data:
        user.show_email = request.data['showEmail']
    if 'showPhone' in request.data:
        user.show_phone = request.data['showPhone']
    if 'showLocation' in request.data:
        user.show_location = request.data['showLocation']
    if 'showActivity' in request.data:
        user.show_activity = request.data['showActivity']

    user.save()

    return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


# NOTA: avatar_view eliminado - ahora se usa /api/media/profile/upload/ (Cloudinary)
