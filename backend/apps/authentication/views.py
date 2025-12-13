from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, GoogleAuthSerializer, SupabaseAuthSerializer
from core.supabase_auth import SupabaseJWTValidator


def get_tokens_for_user(user):
    """Genera tokens JWT para un usuario"""
    refresh = RefreshToken.for_user(user)

    # Obtener el tiempo de expiración del access token desde settings
    access_token_lifetime = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
    expires_in = int(access_token_lifetime.total_seconds()) if access_token_lifetime else 3600

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'expires_in': expires_in,
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
                'expiresIn': tokens['expires_in']
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
                'expiresIn': tokens['expires_in']
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
    """
    Login/Registro con Google OAuth a través de Supabase

    Flujo:
    1. Frontend autentica con Supabase usando signInWithOAuth('google')
    2. Supabase devuelve un access_token JWT al frontend
    3. Frontend envía el access_token a este endpoint
    4. Backend valida el token con el JWT Secret de Supabase
    5. Backend crea o actualiza el usuario en Django
    6. Backend devuelve tokens JWT propios de Django
    """
    serializer = SupabaseAuthSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Datos inválidos'
        }, status=status.HTTP_400_BAD_REQUEST)

    access_token = serializer.validated_data['access_token']

    # Validar el token de Supabase y extraer datos del usuario
    user_data = SupabaseJWTValidator.get_user_data(access_token)

    if not user_data:
        return Response({
            'success': False,
            'message': 'Token de Supabase inválido o expirado'
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Extraer datos específicos de Google
    google_data = SupabaseJWTValidator.extract_google_data(user_data)

    email = google_data.get('email')
    if not email:
        return Response({
            'success': False,
            'message': 'No se pudo obtener el email del usuario'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Crear o actualizar usuario en Django
    try:
        with transaction.atomic():
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': google_data.get('first_name', ''),
                    'last_name': google_data.get('last_name', ''),
                    'google_id': google_data.get('google_id', ''),
                    'avatar': google_data.get('avatar_url') or google_data.get('picture', ''),
                }
            )

            # Si el usuario ya existe, actualizar datos de Google
            if not created:
                # Solo actualizar si los campos están vacíos o si los datos de Google son más completos
                if not user.google_id and google_data.get('google_id'):
                    user.google_id = google_data.get('google_id')

                if not user.first_name and google_data.get('first_name'):
                    user.first_name = google_data.get('first_name')

                if not user.last_name and google_data.get('last_name'):
                    user.last_name = google_data.get('last_name')

                # Actualizar avatar si cambió
                new_avatar = google_data.get('avatar_url') or google_data.get('picture', '')
                if new_avatar and user.avatar != new_avatar:
                    user.avatar = new_avatar

                user.last_login_at = timezone.now()
                user.save()

            # Generar tokens JWT de Django para el usuario
            tokens = get_tokens_for_user(user)

            return Response({
                'success': True,
                'message': 'Autenticación exitosa' if not created else 'Usuario creado exitosamente',
                'user': UserSerializer(user).data,
                'tokens': {
                    'accessToken': tokens['access'],
                    'refreshToken': tokens['refresh'],
                    'tokenType': 'Bearer',
                    'expiresIn': tokens['expires_in']
                },
                'isNewUser': created
            }, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error al crear/actualizar usuario: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
