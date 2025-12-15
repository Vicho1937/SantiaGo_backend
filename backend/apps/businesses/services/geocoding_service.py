"""
Servicio de Geocodificación - RutaLocal Backend

Este módulo proporciona funcionalidad de geocodificación (conversión de direcciones a coordenadas)
usando Mapbox Geocoding API.

Arquitectura:
- GeocodingProvider (ABC): Interface para diferentes proveedores de geocodificación
- MapboxGeocodingProvider: Implementación concreta para Mapbox
- GeocodingService: Servicio principal que utiliza el provider configurado

Autor: Senior Developer
Fecha: 2025-12-15
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


@dataclass
class GeocodingResult:
    """
    Resultado de una operación de geocodificación

    Attributes:
        latitude: Latitud de la ubicación
        longitude: Longitud de la ubicación
        formatted_address: Dirección formateada por el proveedor
        neighborhood: Barrio o vecindario
        comuna: Comuna/municipio
        city: Ciudad
        country: País
        confidence: Nivel de confianza del resultado (0-1)
    """
    latitude: float
    longitude: float
    formatted_address: str
    neighborhood: Optional[str] = None
    comuna: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    confidence: float = 1.0

    def to_dict(self) -> Dict:
        """Convierte el resultado a diccionario"""
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'formatted_address': self.formatted_address,
            'neighborhood': self.neighborhood,
            'comuna': self.comuna,
            'city': self.city,
            'country': self.country,
            'confidence': self.confidence
        }


class GeocodingProvider(ABC):
    """
    Interface abstracta para proveedores de geocodificación

    Permite implementar diferentes proveedores (Mapbox, Google Maps, OpenStreetMap)
    siguiendo el principio Open/Closed de SOLID
    """

    @abstractmethod
    def geocode(self, address: str, context: Optional[str] = None) -> GeocodingResult:
        """
        Geocodifica una dirección

        Args:
            address: Dirección a geocodificar
            context: Contexto geográfico adicional (ciudad, país)

        Returns:
            GeocodingResult con las coordenadas y metadatos

        Raises:
            GeocodingError: Si no se puede geocodificar la dirección
        """
        pass

    @abstractmethod
    def reverse_geocode(self, latitude: float, longitude: float) -> GeocodingResult:
        """
        Reverse geocoding: convierte coordenadas a dirección

        Args:
            latitude: Latitud
            longitude: Longitud

        Returns:
            GeocodingResult con la dirección y metadatos

        Raises:
            GeocodingError: Si no se puede obtener la dirección
        """
        pass


class GeocodingError(Exception):
    """Excepción personalizada para errores de geocodificación"""
    pass


class MapboxGeocodingProvider(GeocodingProvider):
    """
    Implementación de geocodificación usando Mapbox Geocoding API

    Documentación: https://docs.mapbox.com/api/search/geocoding/
    """

    BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"

    def __init__(self, access_token: Optional[str] = None):
        """
        Inicializa el provider de Mapbox

        Args:
            access_token: Token de acceso de Mapbox (opcional, usa settings si no se provee)
        """
        self.access_token = access_token or getattr(settings, 'MAPBOX_ACCESS_TOKEN', None)

        if not self.access_token:
            raise ValueError(
                "MAPBOX_ACCESS_TOKEN no configurado. "
                "Agregue MAPBOX_ACCESS_TOKEN a settings.py o .env"
            )

    def geocode(self, address: str, context: Optional[str] = None) -> GeocodingResult:
        """
        Geocodifica una dirección usando Mapbox

        Args:
            address: Dirección a geocodificar (ej: "Lastarria 305")
            context: Contexto geográfico (ej: "Santiago, Chile")

        Returns:
            GeocodingResult con coordenadas y metadatos

        Raises:
            GeocodingError: Si no se puede geocodificar
        """
        # Construir query completo
        if context:
            query = f"{address}, {context}"
        else:
            query = address

        # Construir URL
        url = f"{self.BASE_URL}/{requests.utils.quote(query)}.json"

        # Parámetros de la API
        params = {
            'access_token': self.access_token,
            'limit': 1,
            'types': 'address,poi',  # Direcciones y puntos de interés
            'language': 'es',  # Respuestas en español
        }

        # Si hay contexto de Santiago, usar bbox para mejorar precisión
        if context and 'Santiago' in context:
            # Bounding box de Santiago, Chile: [min_lng, min_lat, max_lng, max_lat]
            params['bbox'] = '-70.8,-33.6,-70.4,-33.3'

        try:
            logger.info(f"Geocodificando dirección: {query}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            features = data.get('features', [])

            if not features:
                raise GeocodingError(f"No se encontraron resultados para: {query}")

            # Tomar el primer resultado (más relevante)
            feature = features[0]

            # Extraer coordenadas (Mapbox usa [lng, lat])
            coordinates = feature['geometry']['coordinates']
            longitude, latitude = coordinates

            # Extraer metadatos
            place_name = feature.get('place_name', address)
            context_data = feature.get('context', [])

            # Extraer barrio, comuna, ciudad, país del contexto
            neighborhood = self._extract_context_item(context_data, 'neighborhood')
            locality = self._extract_context_item(context_data, 'locality')
            place = self._extract_context_item(context_data, 'place')
            region = self._extract_context_item(context_data, 'region')
            country = self._extract_context_item(context_data, 'country')

            # Determinar comuna (puede venir en locality o place)
            comuna = locality or place

            # Calcular confidence basado en relevance de Mapbox (0-1)
            confidence = feature.get('relevance', 1.0)

            result = GeocodingResult(
                latitude=latitude,
                longitude=longitude,
                formatted_address=place_name,
                neighborhood=neighborhood,
                comuna=comuna,
                city=region or 'Santiago',
                country=country or 'Chile',
                confidence=confidence
            )

            logger.info(f"Geocodificación exitosa: {latitude}, {longitude}")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Error de red al geocodificar: {str(e)}")
            raise GeocodingError(f"Error de conexión con Mapbox API: {str(e)}")
        except (KeyError, IndexError, ValueError) as e:
            logger.error(f"Error al parsear respuesta de Mapbox: {str(e)}")
            raise GeocodingError(f"Error al procesar respuesta de geocodificación: {str(e)}")

    def reverse_geocode(self, latitude: float, longitude: float) -> GeocodingResult:
        """
        Reverse geocoding: convierte coordenadas a dirección

        Args:
            latitude: Latitud
            longitude: Longitud

        Returns:
            GeocodingResult con dirección

        Raises:
            GeocodingError: Si no se puede obtener la dirección
        """
        # Construir URL con coordenadas (Mapbox usa lng,lat)
        url = f"{self.BASE_URL}/{longitude},{latitude}.json"

        params = {
            'access_token': self.access_token,
            'limit': 1,
            'types': 'address,poi',
            'language': 'es',
        }

        try:
            logger.info(f"Reverse geocoding: {latitude}, {longitude}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            features = data.get('features', [])

            if not features:
                raise GeocodingError(
                    f"No se encontró dirección para coordenadas: {latitude}, {longitude}"
                )

            feature = features[0]
            place_name = feature.get('place_name', '')
            context_data = feature.get('context', [])

            neighborhood = self._extract_context_item(context_data, 'neighborhood')
            locality = self._extract_context_item(context_data, 'locality')
            place = self._extract_context_item(context_data, 'place')
            region = self._extract_context_item(context_data, 'region')
            country = self._extract_context_item(context_data, 'country')

            comuna = locality or place

            result = GeocodingResult(
                latitude=latitude,
                longitude=longitude,
                formatted_address=place_name,
                neighborhood=neighborhood,
                comuna=comuna,
                city=region or 'Santiago',
                country=country or 'Chile',
                confidence=feature.get('relevance', 1.0)
            )

            logger.info(f"Reverse geocoding exitoso: {place_name}")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Error de red en reverse geocoding: {str(e)}")
            raise GeocodingError(f"Error de conexión con Mapbox API: {str(e)}")
        except (KeyError, IndexError, ValueError) as e:
            logger.error(f"Error al parsear respuesta de reverse geocoding: {str(e)}")
            raise GeocodingError(f"Error al procesar respuesta: {str(e)}")

    def _extract_context_item(self, context: list, item_type: str) -> Optional[str]:
        """
        Extrae un item específico del contexto de Mapbox

        Args:
            context: Lista de contexto de Mapbox
            item_type: Tipo de item a extraer (neighborhood, locality, place, etc.)

        Returns:
            Texto del item o None si no existe
        """
        for item in context:
            if item.get('id', '').startswith(item_type):
                return item.get('text')
        return None


class GeocodingService:
    """
    Servicio principal de geocodificación

    Utiliza un provider configurable para geocodificar direcciones.
    Implementa patrón Strategy para permitir cambiar el provider sin modificar el servicio.

    Uso:
        service = GeocodingService()
        result = service.geocode_address("Lastarria 305, Santiago")
        print(result.latitude, result.longitude)
    """

    def __init__(self, provider: Optional[GeocodingProvider] = None):
        """
        Inicializa el servicio de geocodificación

        Args:
            provider: Provider de geocodificación (usa Mapbox por defecto)
        """
        self.provider = provider or MapboxGeocodingProvider()

    def geocode_address(
        self,
        address: str,
        city: str = "Santiago, Chile"
    ) -> GeocodingResult:
        """
        Geocodifica una dirección

        Args:
            address: Dirección a geocodificar
            city: Ciudad/país para contexto (default: Santiago, Chile)

        Returns:
            GeocodingResult con coordenadas y metadatos

        Raises:
            GeocodingError: Si no se puede geocodificar

        Example:
            >>> service = GeocodingService()
            >>> result = service.geocode_address("Lastarria 305")
            >>> print(f"{result.latitude}, {result.longitude}")
            -33.437198, -70.638956
        """
        if not address or not address.strip():
            raise GeocodingError("La dirección no puede estar vacía")

        return self.provider.geocode(address.strip(), context=city)

    def reverse_geocode(
        self,
        latitude: float,
        longitude: float
    ) -> GeocodingResult:
        """
        Obtiene la dirección de unas coordenadas

        Args:
            latitude: Latitud
            longitude: Longitud

        Returns:
            GeocodingResult con dirección

        Raises:
            GeocodingError: Si no se puede obtener la dirección

        Example:
            >>> service = GeocodingService()
            >>> result = service.reverse_geocode(-33.437198, -70.638956)
            >>> print(result.formatted_address)
            Lastarria 305, Santiago Centro, Santiago, Chile
        """
        return self.provider.reverse_geocode(latitude, longitude)

    def validate_coordinates(
        self,
        latitude: float,
        longitude: float,
        expected_city: str = "Santiago"
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida que unas coordenadas estén en la ciudad esperada

        Args:
            latitude: Latitud a validar
            longitude: Longitud a validar
            expected_city: Ciudad esperada (default: Santiago)

        Returns:
            Tupla (es_válido, mensaje_error)

        Example:
            >>> service = GeocodingService()
            >>> valid, error = service.validate_coordinates(-33.437198, -70.638956)
            >>> if not valid:
            ...     print(error)
        """
        try:
            result = self.reverse_geocode(latitude, longitude)

            # Verificar que la ciudad coincida
            if result.city and expected_city.lower() in result.city.lower():
                return True, None
            else:
                return False, (
                    f"Las coordenadas están en {result.city or 'ubicación desconocida'}, "
                    f"se esperaba {expected_city}"
                )

        except GeocodingError as e:
            return False, f"No se pudo validar las coordenadas: {str(e)}"
