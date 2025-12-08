"""
Servicio de gestión de imágenes con Cloudinary
"""
import os
import cloudinary
import cloudinary.uploader
from django.conf import settings
from typing import Dict, Optional


class CloudinaryService:
    """Servicio para gestión de imágenes con Cloudinary"""

    def __init__(self):
        """Inicializa la configuración de Cloudinary"""
        cloudinary.config(
            cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
            api_key=os.getenv('CLOUDINARY_API_KEY'),
            api_secret=os.getenv('CLOUDINARY_API_SECRET'),
            secure=True
        )

    def upload_profile_picture(self, file, user_id: int) -> Dict[str, str]:
        """
        Sube una foto de perfil a Cloudinary

        Args:
            file: Archivo de imagen
            user_id: ID del usuario

        Returns:
            Dict con url, secure_url y public_id de la imagen
        """
        try:
            # Upload con transformaciones optimizadas para avatares
            result = cloudinary.uploader.upload(
                file,
                folder=f"rutago/profiles",
                public_id=f"user_{user_id}",
                overwrite=True,
                transformation=[
                    {'width': 400, 'height': 400, 'crop': 'fill', 'gravity': 'face'},
                    {'quality': 'auto:good'},
                    {'fetch_format': 'auto'}
                ],
                eager=[
                    # Thumbnail pequeño para listas
                    {'width': 100, 'height': 100, 'crop': 'thumb', 'gravity': 'face'}
                ]
            )

            return {
                'url': result['secure_url'],
                'thumbnail_url': result['eager'][0]['secure_url'] if result.get('eager') else result['secure_url'],
                'public_id': result['public_id']
            }
        except Exception as e:
            raise Exception(f"Error al subir foto de perfil: {str(e)}")

    def upload_business_photo(self, file, business_id: int, photo_index: int = 0) -> Dict[str, str]:
        """
        Sube una foto de negocio a Cloudinary

        Args:
            file: Archivo de imagen
            business_id: ID del negocio
            photo_index: Índice de la foto (para múltiples fotos)

        Returns:
            Dict con url, secure_url y public_id de la imagen
        """
        try:
            result = cloudinary.uploader.upload(
                file,
                folder=f"rutago/businesses/{business_id}",
                public_id=f"photo_{photo_index}",
                overwrite=True,
                transformation=[
                    {'width': 1200, 'height': 800, 'crop': 'fill'},
                    {'quality': 'auto:good'},
                    {'fetch_format': 'auto'}
                ],
                eager=[
                    # Thumbnail para previews
                    {'width': 400, 'height': 300, 'crop': 'fill'},
                    # Thumbnail pequeño para cards
                    {'width': 200, 'height': 150, 'crop': 'fill'}
                ]
            )

            return {
                'url': result['secure_url'],
                'thumbnail_url': result['eager'][0]['secure_url'] if result.get('eager') else result['secure_url'],
                'small_thumbnail_url': result['eager'][1]['secure_url'] if len(result.get('eager', [])) > 1 else result['secure_url'],
                'public_id': result['public_id']
            }
        except Exception as e:
            raise Exception(f"Error al subir foto de negocio: {str(e)}")

    def delete_image(self, public_id: str) -> bool:
        """
        Elimina una imagen de Cloudinary

        Args:
            public_id: ID público de la imagen en Cloudinary

        Returns:
            True si se eliminó correctamente
        """
        try:
            result = cloudinary.uploader.destroy(public_id)
            return result.get('result') == 'ok'
        except Exception as e:
            raise Exception(f"Error al eliminar imagen: {str(e)}")

    def get_image_url(self, public_id: str, transformation: Optional[Dict] = None) -> str:
        """
        Obtiene la URL de una imagen con transformaciones opcionales

        Args:
            public_id: ID público de la imagen
            transformation: Dict con parámetros de transformación

        Returns:
            URL de la imagen
        """
        try:
            if transformation:
                return cloudinary.CloudinaryImage(public_id).build_url(**transformation)
            return cloudinary.CloudinaryImage(public_id).build_url()
        except Exception as e:
            raise Exception(f"Error al obtener URL de imagen: {str(e)}")


# Función para obtener instancia del servicio (lazy loading)
_cloudinary_service_instance = None

def get_cloudinary_service():
    """Obtiene la instancia del servicio Cloudinary (lazy loading)"""
    global _cloudinary_service_instance
    if _cloudinary_service_instance is None:
        _cloudinary_service_instance = CloudinaryService()
    return _cloudinary_service_instance
