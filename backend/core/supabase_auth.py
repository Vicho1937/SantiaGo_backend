"""
Utilidades para validar tokens JWT de Supabase Auth
"""
import jwt
from django.conf import settings
from typing import Optional, Dict, Any


class SupabaseJWTValidator:
    """
    Valida y decodifica tokens JWT emitidos por Supabase Auth
    """

    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Decodifica y valida un token JWT de Supabase

        Args:
            token: El token JWT a validar

        Returns:
            Dict con los datos del token si es válido, None si no es válido
        """
        try:
            # Decodificar el token usando el JWT secret de Supabase
            decoded = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=['HS256'],
                audience='authenticated',
                options={
                    'verify_signature': True,
                    'verify_exp': True,
                    'verify_aud': True,
                }
            )

            return decoded

        except jwt.ExpiredSignatureError:
            print("Token expirado")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Token inválido: {e}")
            return None
        except Exception as e:
            print(f"Error al decodificar token: {e}")
            return None

    @staticmethod
    def get_user_data(token: str) -> Optional[Dict[str, Any]]:
        """
        Extrae los datos del usuario del token JWT de Supabase

        Args:
            token: El token JWT

        Returns:
            Dict con los datos del usuario si el token es válido
        """
        decoded = SupabaseJWTValidator.decode_token(token)

        if not decoded:
            return None

        # Extraer datos relevantes del usuario
        user_data = {
            'supabase_id': decoded.get('sub'),  # ID del usuario en Supabase
            'email': decoded.get('email'),
            'email_verified': decoded.get('email_confirmed_at') is not None,
            'provider': decoded.get('app_metadata', {}).get('provider'),  # google, email, etc.
            'user_metadata': decoded.get('user_metadata', {}),  # metadata del proveedor (Google)
            'role': decoded.get('role', 'authenticated'),
        }

        return user_data

    @staticmethod
    def extract_google_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrae datos específicos de Google del metadata de Supabase

        Args:
            user_data: Datos del usuario extraídos del token

        Returns:
            Dict con datos de Google (nombre, avatar, etc.)
        """
        user_metadata = user_data.get('user_metadata', {})

        google_data = {
            'email': user_data.get('email'),
            'full_name': user_metadata.get('full_name', ''),
            'first_name': user_metadata.get('given_name', ''),
            'last_name': user_metadata.get('family_name', ''),
            'avatar_url': user_metadata.get('avatar_url', ''),
            'picture': user_metadata.get('picture', ''),
            'google_id': user_metadata.get('provider_id', ''),
        }

        return google_data
