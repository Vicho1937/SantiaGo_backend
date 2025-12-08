"""
Utilidades comunes para el proyecto
"""
from math import radians, cos, sin, asin, sqrt
from datetime import datetime
from django.db.models import Q


def haversine_distance(lon1, lat1, lon2, lat2):
    """
    Calcular distancia entre dos puntos usando fórmula Haversine
    
    Args:
        lon1, lat1: Coordenadas del punto 1
        lon2, lat2: Coordenadas del punto 2
    
    Returns:
        Distancia en kilómetros
    """
    # Convertir grados a radianes
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
    
    # Fórmula Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radio de la Tierra en kilómetros
    km = 6371 * c
    
    return round(km, 2)


def is_business_open_now(business):
    """
    Verificar si un negocio está abierto en el momento actual
    
    Args:
        business: Instancia de Business model
    
    Returns:
        Tuple (is_open: bool, closes_at: str or None)
    """
    if business.is_open_24h:
        return True, None
    
    if not business.hours:
        return False, None
    
    now = datetime.now()
    day_name = now.strftime('%A').lower()  # 'monday', 'tuesday', etc.
    current_time = now.strftime('%H:%M')
    
    # Verificar si hay horario para hoy
    if day_name not in business.hours:
        return False, None
    
    day_hours = business.hours[day_name]
    
    # Verificar si el negocio está cerrado todo el día
    if not day_hours.get('open') or not day_hours.get('close'):
        return False, None
    
    open_time = day_hours['open']
    close_time = day_hours['close']
    
    # Comparar tiempos
    is_open = open_time <= current_time <= close_time
    
    return is_open, close_time if is_open else None


def filter_businesses_by_location(queryset, lat, lng, radius=5):
    """
    Filtrar negocios por distancia desde un punto
    
    Args:
        queryset: QuerySet de Business
        lat: Latitud del centro
        lng: Longitud del centro
        radius: Radio en kilómetros
    
    Returns:
        Lista de (business, distance) tuplas dentro del radio
    """
    businesses_with_distance = []
    
    for business in queryset:
        distance = haversine_distance(
            lng, lat,
            float(business.longitude), float(business.latitude)
        )
        
        if distance <= radius:
            businesses_with_distance.append((business, distance))
    
    # Ordenar por distancia
    businesses_with_distance.sort(key=lambda x: x[1])
    
    return businesses_with_distance


def search_businesses(queryset, query):
    """
    Búsqueda de texto en negocios
    
    Args:
        queryset: QuerySet de Business
        query: Término de búsqueda
    
    Returns:
        QuerySet filtrado
    """
    if not query:
        return queryset
    
    return queryset.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(short_description__icontains=query) |
        Q(neighborhood__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()


def calculate_route_stats(stops):
    """
    Calcular estadísticas de una ruta
    
    Args:
        stops: QuerySet o lista de RouteStop
    
    Returns:
        Dict con total_distance, estimated_duration, stops_count
    """
    if not stops:
        return {
            'total_distance': 0,
            'estimated_duration': 0,
            'stops_count': 0
        }
    
    total_distance = 0
    total_duration = 0
    
    # Calcular distancia entre paradas consecutivas
    stops_list = list(stops.order_by('order'))
    
    for i in range(len(stops_list) - 1):
        current = stops_list[i]
        next_stop = stops_list[i + 1]
        
        distance = haversine_distance(
            float(current.business.longitude),
            float(current.business.latitude),
            float(next_stop.business.longitude),
            float(next_stop.business.latitude)
        )
        
        total_distance += distance
        total_duration += current.duration
    
    # Agregar duración de la última parada
    if stops_list:
        total_duration += stops_list[-1].duration
    
    # Agregar tiempo estimado de traslado (5 min por km)
    travel_time = int(total_distance * 5)
    total_duration += travel_time
    
    return {
        'total_distance': round(total_distance, 2),
        'estimated_duration': total_duration,
        'stops_count': len(stops_list)
    }
