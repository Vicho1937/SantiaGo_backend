"""
Validadores para la app de negocios

Proporciona validadores reutilizables para coordenadas, direcciones y ubicaciones.

Autor: Senior Developer
Fecha: 2025-12-15
"""

from typing import Tuple, Optional
from django.core.exceptions import ValidationError
from decimal import Decimal
import re


class CoordinateValidator:
    """
    Validador para coordenadas geográficas

    Valida rangos válidos de latitud y longitud según estándares WGS84
    """

    # Rangos válidos según WGS84
    MIN_LATITUDE = -90.0
    MAX_LATITUDE = 90.0
    MIN_LONGITUDE = -180.0
    MAX_LONGITUDE = 180.0

    @classmethod
    def validate_latitude(cls, value: float) -> None:
        """
        Valida que la latitud esté en rango válido

        Args:
            value: Latitud a validar

        Raises:
            ValidationError: Si la latitud está fuera de rango
        """
        if not isinstance(value, (int, float, Decimal)):
            raise ValidationError(
                f"Latitud debe ser un número, se recibió: {type(value).__name__}"
            )

        lat = float(value)

        if lat < cls.MIN_LATITUDE or lat > cls.MAX_LATITUDE:
            raise ValidationError(
                f"Latitud debe estar entre {cls.MIN_LATITUDE} y {cls.MAX_LATITUDE}, "
                f"se recibió: {lat}"
            )

    @classmethod
    def validate_longitude(cls, value: float) -> None:
        """
        Valida que la longitud esté en rango válido

        Args:
            value: Longitud a validar

        Raises:
            ValidationError: Si la longitud está fuera de rango
        """
        if not isinstance(value, (int, float, Decimal)):
            raise ValidationError(
                f"Longitud debe ser un número, se recibió: {type(value).__name__}"
            )

        lng = float(value)

        if lng < cls.MIN_LONGITUDE or lng > cls.MAX_LONGITUDE:
            raise ValidationError(
                f"Longitud debe estar entre {cls.MIN_LONGITUDE} y {cls.MAX_LONGITUDE}, "
                f"se recibió: {lng}"
            )

    @classmethod
    def validate_coordinates(cls, latitude: float, longitude: float) -> None:
        """
        Valida un par de coordenadas

        Args:
            latitude: Latitud
            longitude: Longitud

        Raises:
            ValidationError: Si alguna coordenada es inválida
        """
        cls.validate_latitude(latitude)
        cls.validate_longitude(longitude)


class SantiagoLocationValidator:
    """
    Validador especializado para ubicaciones en Santiago, Chile

    Define bounding box de Santiago para validar que las coordenadas
    estén dentro del área metropolitana
    """

    # Bounding box aproximado de Santiago, Chile
    # [min_lat, max_lat, min_lng, max_lng]
    SANTIAGO_BBOX = {
        'min_lat': -33.7,  # Sur
        'max_lat': -33.3,  # Norte
        'min_lng': -70.9,  # Oeste
        'max_lng': -70.4,  # Este
    }

    # Nombre de la ciudad
    CITY_NAME = "Santiago"
    COUNTRY_NAME = "Chile"

    @classmethod
    def is_in_santiago(cls, latitude: float, longitude: float) -> bool:
        """
        Verifica si unas coordenadas están dentro de Santiago

        Args:
            latitude: Latitud a verificar
            longitude: Longitud a verificar

        Returns:
            True si las coordenadas están en Santiago, False en caso contrario
        """
        lat = float(latitude)
        lng = float(longitude)

        return (
            cls.SANTIAGO_BBOX['min_lat'] <= lat <= cls.SANTIAGO_BBOX['max_lat'] and
            cls.SANTIAGO_BBOX['min_lng'] <= lng <= cls.SANTIAGO_BBOX['max_lng']
        )

    @classmethod
    def validate_location(cls, latitude: float, longitude: float) -> None:
        """
        Valida que unas coordenadas estén en Santiago

        Args:
            latitude: Latitud
            longitude: Longitud

        Raises:
            ValidationError: Si las coordenadas no están en Santiago
        """
        # Primero validar que sean coordenadas válidas
        CoordinateValidator.validate_coordinates(latitude, longitude)

        # Luego validar que estén en Santiago
        if not cls.is_in_santiago(latitude, longitude):
            raise ValidationError(
                f"Las coordenadas ({latitude}, {longitude}) no están en Santiago, Chile. "
                f"Por favor verifica la dirección."
            )

    @classmethod
    def get_distance_from_center(cls, latitude: float, longitude: float) -> float:
        """
        Calcula la distancia aproximada desde el centro de Santiago

        Args:
            latitude: Latitud
            longitude: Longitud

        Returns:
            Distancia en kilómetros desde el centro de Santiago

        Note:
            Usa el centro aproximado de Santiago: Plaza de Armas
            (-33.4372, -70.6506)
        """
        from apps.businesses.utils import haversine_distance

        # Centro de Santiago (Plaza de Armas)
        SANTIAGO_CENTER_LAT = -33.4372
        SANTIAGO_CENTER_LNG = -70.6506

        return haversine_distance(
            longitude, latitude,
            SANTIAGO_CENTER_LNG, SANTIAGO_CENTER_LAT
        )


class AddressValidator:
    """
    Validador para direcciones chilenas

    Valida formato y contenido de direcciones
    """

    # Patrones comunes de direcciones en Chile
    STREET_TYPES = [
        'calle', 'avenida', 'av', 'pasaje', 'psje',
        'camino', 'callejón', 'callejon', 'paseo'
    ]

    MIN_ADDRESS_LENGTH = 5
    MAX_ADDRESS_LENGTH = 255

    @classmethod
    def validate_address(cls, address: str) -> None:
        """
        Valida que una dirección tenga formato correcto

        Args:
            address: Dirección a validar

        Raises:
            ValidationError: Si la dirección es inválida
        """
        if not address or not address.strip():
            raise ValidationError("La dirección no puede estar vacía")

        address = address.strip()

        # Validar longitud
        if len(address) < cls.MIN_ADDRESS_LENGTH:
            raise ValidationError(
                f"La dirección debe tener al menos {cls.MIN_ADDRESS_LENGTH} caracteres"
            )

        if len(address) > cls.MAX_ADDRESS_LENGTH:
            raise ValidationError(
                f"La dirección no puede exceder {cls.MAX_ADDRESS_LENGTH} caracteres"
            )

        # Validar que contenga al menos un número (numeración de calle)
        if not re.search(r'\d', address):
            raise ValidationError(
                "La dirección debe incluir una numeración (ej: 'Lastarria 305')"
            )

    @classmethod
    def normalize_address(cls, address: str) -> str:
        """
        Normaliza una dirección para geocodificación

        Args:
            address: Dirección a normalizar

        Returns:
            Dirección normalizada

        Example:
            >>> AddressValidator.normalize_address("  av. libertador  123  ")
            "Avenida Libertador 123"
        """
        if not address:
            return ""

        # Eliminar espacios extras
        normalized = " ".join(address.split())

        # Capitalizar primera letra de cada palabra
        normalized = normalized.title()

        # Expandir abreviaciones comunes
        replacements = {
            r'\bAv\b\.?': 'Avenida',
            r'\bPsje\b\.?': 'Pasaje',
            r'\bCno\b\.?': 'Camino',
        }

        for pattern, replacement in replacements.items():
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

        return normalized


class BusinessLocationValidator:
    """
    Validador completo para ubicación de negocios

    Combina validación de coordenadas, dirección y ubicación en Santiago
    """

    @classmethod
    def validate_business_location(
        cls,
        address: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        require_coordinates: bool = False
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida la ubicación completa de un negocio

        Args:
            address: Dirección del negocio
            latitude: Latitud (opcional)
            longitude: Longitud (opcional)
            require_coordinates: Si True, las coordenadas son obligatorias

        Returns:
            Tupla (es_válido, mensaje_error)

        Example:
            >>> validator = BusinessLocationValidator()
            >>> valid, error = validator.validate_business_location(
            ...     "Lastarria 305",
            ...     -33.437198,
            ...     -70.638956
            ... )
            >>> if not valid:
            ...     print(error)
        """
        try:
            # Validar dirección
            AddressValidator.validate_address(address)

            # Si se proveen coordenadas, validarlas
            if latitude is not None and longitude is not None:
                CoordinateValidator.validate_coordinates(latitude, longitude)
                SantiagoLocationValidator.validate_location(latitude, longitude)
            elif require_coordinates:
                return False, "Se requieren coordenadas (latitud y longitud)"

            return True, None

        except ValidationError as e:
            return False, str(e)

    @classmethod
    def prepare_for_geocoding(cls, address: str, comuna: Optional[str] = None) -> str:
        """
        Prepara una dirección para geocodificación

        Args:
            address: Dirección base
            comuna: Comuna (opcional)

        Returns:
            Dirección formateada para geocodificación

        Example:
            >>> BusinessLocationValidator.prepare_for_geocoding(
            ...     "Lastarria 305",
            ...     "Santiago Centro"
            ... )
            "Lastarria 305, Santiago Centro, Santiago, Chile"
        """
        # Normalizar dirección
        normalized = AddressValidator.normalize_address(address)

        # Construir dirección completa para geocodificación
        parts = [normalized]

        if comuna:
            parts.append(comuna)

        parts.extend(["Santiago", "Chile"])

        return ", ".join(parts)
