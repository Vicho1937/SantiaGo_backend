"""
Vistas para gestión de media (imágenes)
"""
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .services import get_cloudinary_service
from .serializers import ProfilePictureUploadSerializer, BusinessPhotoUploadSerializer
from apps.authentication.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_profile_picture(request):
    """
    Endpoint para subir foto de perfil del usuario autenticado

    Body (multipart/form-data):
    - image: archivo de imagen (JPEG, PNG, WEBP)
    """
    serializer = ProfilePictureUploadSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'error': serializer.errors,
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        cloudinary_service = get_cloudinary_service()
        image_file = serializer.validated_data['image']

        # Subir imagen a Cloudinary
        result = cloudinary_service.upload_profile_picture(
            file=image_file,
            user_id=request.user.id
        )

        # Actualizar avatar del usuario
        user = request.user
        user.avatar = result['url']
        user.avatar_thumbnail = result['thumbnail_url']
        user.save(update_fields=['avatar', 'avatar_thumbnail'])

        return Response({
            'success': True,
            'message': 'Foto de perfil actualizada correctamente',
            'data': {
                'avatar': result['url'],
                'avatar_thumbnail': result['thumbnail_url'],
                'public_id': result['public_id']
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_business_photo_temp(request):
    """
    Endpoint para subir fotos temporales de negocios (antes de crear el negocio)
    
    Body (multipart/form-data):
    - image: archivo de imagen
    """
    serializer = BusinessPhotoUploadSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'error': serializer.errors,
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        cloudinary_service = get_cloudinary_service()
        image_file = serializer.validated_data['image']
        
        # Subir imagen a Cloudinary con un identificador temporal
        import uuid
        temp_id = str(uuid.uuid4())
        result = cloudinary_service.upload_business_photo(
            file=image_file,
            business_id=temp_id,
            photo_index=0
        )
        
        return Response({
            'success': True,
            'message': 'Imagen subida correctamente',
            'data': {
                'url': result['url'],
                'thumbnail_url': result['thumbnail_url'],
                'small_thumbnail_url': result.get('small_thumbnail_url'),
                'public_id': result['public_id']
            }
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"❌ Error uploading business photo: {error_detail}")
        return Response({
            'error': str(e),
            'error_detail': error_detail if settings.DEBUG else None,
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_business_photo(request, business_id):
    """
    Endpoint para subir fotos de un negocio

    Solo usuarios con permisos (dueño del negocio o admin)

    Body (multipart/form-data):
    - image: archivo de imagen
    - photo_index: índice de la foto (0-10)
    """
    # Verificar que el negocio existe y el usuario tiene permisos
    from apps.businesses.models import Business

    try:
        business = Business.objects.get(id=business_id)
    except Business.DoesNotExist:
        return Response({
            'error': 'Negocio no encontrado',
            'success': False
        }, status=status.HTTP_404_NOT_FOUND)

    # Verificar permisos (solo owner o admin)
    if business.owner != request.user and not request.user.is_staff:
        return Response({
            'error': 'No tienes permisos para subir fotos a este negocio',
            'success': False
        }, status=status.HTTP_403_FORBIDDEN)

    serializer = BusinessPhotoUploadSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'error': serializer.errors,
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        cloudinary_service = get_cloudinary_service()
        image_file = serializer.validated_data['image']
        photo_index = serializer.validated_data.get('photo_index', 0)

        # Subir imagen a Cloudinary
        result = cloudinary_service.upload_business_photo(
            file=image_file,
            business_id=business_id,
            photo_index=photo_index
        )

        # TODO: Actualizar modelo Business con las URLs de las fotos
        # Por ahora solo retornamos las URLs

        return Response({
            'success': True,
            'message': 'Foto del negocio subida correctamente',
            'data': {
                'url': result['url'],
                'thumbnail_url': result['thumbnail_url'],
                'small_thumbnail_url': result['small_thumbnail_url'],
                'public_id': result['public_id'],
                'photo_index': photo_index
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile_picture(request):
    """
    Endpoint para eliminar foto de perfil del usuario autenticado
    """
    try:
        user = request.user

        if not user.avatar:
            return Response({
                'error': 'No tienes foto de perfil para eliminar',
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)

        # Eliminar de Cloudinary (extraer public_id de la URL)
        # Format: https://res.cloudinary.com/{cloud_name}/image/upload/v{version}/{public_id}.{format}
        if 'cloudinary.com' in user.avatar:
            cloudinary_service = get_cloudinary_service()
            public_id = f"rutago/profiles/user_{user.id}"
            cloudinary_service.delete_image(public_id)

        # Limpiar campos de avatar
        user.avatar = ''
        user.avatar_thumbnail = ''
        user.save(update_fields=['avatar', 'avatar_thumbnail'])

        return Response({
            'success': True,
            'message': 'Foto de perfil eliminada correctamente'
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
