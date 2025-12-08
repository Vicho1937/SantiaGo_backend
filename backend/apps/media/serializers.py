"""
Serializers para gestión de media
"""
from rest_framework import serializers


class ProfilePictureUploadSerializer(serializers.Serializer):
    """Serializer para upload de foto de perfil"""
    image = serializers.ImageField(required=True)

    def validate_image(self, value):
        """Valida el archivo de imagen"""
        # Validar tamaño (máximo 5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("La imagen no puede superar los 5MB")

        # Validar formato
        valid_formats = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
        if value.content_type not in valid_formats:
            raise serializers.ValidationError(
                f"Formato no válido. Use: {', '.join(valid_formats)}"
            )

        return value


class BusinessPhotoUploadSerializer(serializers.Serializer):
    """Serializer para upload de fotos de negocio"""
    image = serializers.ImageField(required=True)
    photo_index = serializers.IntegerField(default=0, min_value=0, max_value=10)

    def validate_image(self, value):
        """Valida el archivo de imagen"""
        # Validar tamaño (máximo 10MB para fotos de negocios)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("La imagen no puede superar los 10MB")

        # Validar formato
        valid_formats = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
        if value.content_type not in valid_formats:
            raise serializers.ValidationError(
                f"Formato no válido. Use: {', '.join(valid_formats)}"
            )

        return value


class ImageResponseSerializer(serializers.Serializer):
    """Serializer para respuesta de imagen subida"""
    url = serializers.URLField()
    thumbnail_url = serializers.URLField(required=False)
    small_thumbnail_url = serializers.URLField(required=False)
    public_id = serializers.CharField()
