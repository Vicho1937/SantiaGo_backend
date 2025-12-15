from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import Business, Category, Feature, Favorite, Visit, BusinessOwnerProfile
from .serializers import (
    BusinessListSerializer, BusinessDetailSerializer,
    CategorySerializer, FeatureSerializer, FavoriteSerializer, VisitSerializer,
    BusinessOwnerProfileSerializer, BusinessCreateSerializer
)


class CategoryListView(generics.ListAPIView):
    """Listar todas las categorías"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BusinessListView(generics.ListAPIView):
    """Listar negocios con filtros"""
    serializer_class = BusinessListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'neighborhood']
    ordering_fields = ['rating', 'review_count', 'created_at']
    
    def get_queryset(self):
        queryset = Business.objects.filter(is_active=True, status='published').select_related('category').prefetch_related('features')
        
        # Filtro por categoría
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filtro por barrio
        neighborhood = self.request.query_params.get('neighborhood')
        if neighborhood:
            queryset = queryset.filter(neighborhood__iexact=neighborhood)
        
        # Filtro por rating mínimo
        rating_min = self.request.query_params.get('rating_min')
        if rating_min:
            queryset = queryset.filter(rating__gte=rating_min)
        
        # Filtro por rango de precio
        price_range = self.request.query_params.get('price_range')
        if price_range:
            queryset = queryset.filter(price_range=price_range)
        
        # Filtro por features
        features = self.request.query_params.get('features')
        if features:
            feature_list = features.split(',')
            for feature in feature_list:
                queryset = queryset.filter(features__slug=feature)
        
        # Filtro por búsqueda de texto
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(neighborhood__icontains=search)
            )
        
        # Ordenamiento por distancia si se proporciona lat/lng
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        if lat and lng:
            # TODO: Implementar ordenamiento por distancia
            pass
        
        return queryset.distinct()
    
    def get_serializer_context(self):
        """Pasar lat/lng al serializer para cálculo de distancia"""
        context = super().get_serializer_context()
        context['user_lat'] = self.request.query_params.get('lat')
        context['user_lng'] = self.request.query_params.get('lng')
        return context
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            
            return Response({
                'success': True,
                'data': {
                    'results': paginated_response.data['results'],
                    'pagination': {
                        'page': request.query_params.get('page', 1),
                        'per_page': self.pagination_class.page_size,
                        'total': paginated_response.data['count'],
                        'pages': (paginated_response.data['count'] + self.pagination_class.page_size - 1) // self.pagination_class.page_size
                    }
                }
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


class BusinessDetailView(generics.RetrieveAPIView):
    """Detalle de un negocio"""
    queryset = Business.objects.filter(is_active=True)
    serializer_class = BusinessDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Incrementar contador de vistas
        Business.objects.filter(id=instance.id).update(views=models.F('views') + 1)
        
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_business(request, business_id):
    """Agregar negocio a favoritos"""
    try:
        business = Business.objects.get(id=business_id, is_active=True)
    except Business.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Negocio no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        business=business
    )
    
    if created:
        # Incrementar contador
        Business.objects.filter(id=business_id).update(favorites_count=models.F('favorites_count') + 1)
        
        return Response({
            'success': True,
            'message': 'Negocio agregado a favoritos'
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': True,
        'message': 'El negocio ya está en favoritos'
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unfavorite_business(request, business_id):
    """Quitar negocio de favoritos"""
    try:
        favorite = Favorite.objects.get(
            user=request.user,
            business_id=business_id
        )
        favorite.delete()
        
        # Decrementar contador
        Business.objects.filter(id=business_id).update(favorites_count=models.F('favorites_count') - 1)
        
        return Response({
            'success': True,
            'message': 'Negocio eliminado de favoritos'
        }, status=status.HTTP_200_OK)
    
    except Favorite.DoesNotExist:
        return Response({
            'success': False,
            'message': 'El negocio no está en favoritos'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_visit(request, business_id):
    """Registrar visita a un negocio"""
    try:
        business = Business.objects.get(id=business_id, is_active=True)
    except Business.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Negocio no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    visit = Visit.objects.create(
        user=request.user,
        business=business,
        notes=request.data.get('notes', '')
    )
    
    # Incrementar contadores
    Business.objects.filter(id=business_id).update(visits_count=models.F('visits_count') + 1)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    User.objects.filter(id=request.user.id).update(businesses_visited=models.F('businesses_visited') + 1)
    
    return Response({
        'success': True,
        'data': VisitSerializer(visit).data,
        'message': 'Visita registrada exitosamente'
    }, status=status.HTTP_201_CREATED)


# Import models for F expressions
from django.db import models


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def owner_profile(request):
    """Obtener perfil de propietario del usuario actual"""
    profile, created = BusinessOwnerProfile.objects.get_or_create(user=request.user)
    serializer = BusinessOwnerProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_my_business(request):
    """Crear un negocio (solo usuarios con permisos)"""
    profile, created = BusinessOwnerProfile.objects.get_or_create(user=request.user)

    if not profile.can_create_more:
        return Response({
            'error': 'No tienes permiso para crear más negocios',
            'max_allowed': profile.max_businesses_allowed,
            'created': profile.businesses_created_count
        }, status=status.HTTP_403_FORBIDDEN)

    serializer = BusinessCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        business = serializer.save()

        # Mensaje dinámico basado en el estado del negocio
        if business.status == 'published':
            message = 'Negocio creado y publicado exitosamente. Ya es visible para todos los usuarios.'
        else:
            message = 'Negocio creado exitosamente. Está pendiente de revisión por un administrador.'

        return Response({
            'success': True,
            'message': message,
            'business': BusinessDetailSerializer(business).data,
            'status': business.status
        }, status=status.HTTP_201_CREATED)

    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_businesses(request):
    """Listar todos mis negocios"""
    businesses = Business.objects.filter(owner=request.user, created_by_owner=True)
    serializer = BusinessListSerializer(businesses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_business_dashboard(request, business_id):
    """Dashboard con estadísticas de mi negocio"""
    try:
        business = Business.objects.get(id=business_id, owner=request.user)
    except Business.DoesNotExist:
        return Response({'error': 'Negocio no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    from apps.reviews.models import Review
    recent_reviews = Review.objects.filter(business=business, is_approved=True).order_by('-created_at')[:5]

    return Response({
        'business': BusinessDetailSerializer(business).data,
        'stats': {
            'views': business.views,
            'rating': float(business.rating),
            'review_count': business.review_count,
            'favorites_count': business.favorites_count,
            'visits_count': business.visits_count,
            'status': business.status,
        },
        'recent_reviews': [{
            'user': review.user.email,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at
        } for review in recent_reviews]
    })


@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def update_my_business(request, business_id):
    """
    Actualizar información de mi negocio.
    Solo el propietario puede actualizar su negocio.
    """
    try:
        business = Business.objects.get(id=business_id, owner=request.user, created_by_owner=True)
    except Business.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Negocio no encontrado o no tienes permisos para editarlo'
        }, status=status.HTTP_404_NOT_FOUND)

    # Campos permitidos para actualización
    allowed_fields = [
        'name', 'description', 'short_description', 'address', 'neighborhood',
        'comuna', 'phone', 'email', 'website', 'instagram', 'latitude', 'longitude',
        'hours', 'is_open_24h', 'price_range', 'cover_image', 'images', 'logo'
    ]

    # Actualizar solo los campos proporcionados
    for field in allowed_fields:
        if field in request.data:
            setattr(business, field, request.data[field])

    # Manejar category si viene como slug, UUID, o objeto
    if 'category' in request.data:
        from .models import Category
        category_data = request.data['category']

        try:
            # Si viene como diccionario/objeto, extraer slug o id
            if isinstance(category_data, dict):
                category_slug = category_data.get('slug') or category_data.get('id')
                if not category_slug:
                    return Response({
                        'success': False,
                        'error': 'La categoría debe incluir "slug" o "id"'
                    }, status=status.HTTP_400_BAD_REQUEST)
                category_data = category_slug

            # Ahora category_data es un string (slug o UUID)
            if isinstance(category_data, str):
                # Intentar primero por slug
                category = Category.objects.filter(slug=category_data).first()
                if not category:
                    # Intentar por UUID
                    try:
                        category = Category.objects.get(id=category_data)
                    except (Category.DoesNotExist, ValueError):
                        return Response({
                            'success': False,
                            'error': f"Categoría '{category_data}' no encontrada"
                        }, status=status.HTTP_400_BAD_REQUEST)
                business.category = category
            else:
                return Response({
                    'success': False,
                    'error': 'Formato de categoría inválido'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error al procesar categoría: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

    # Manejar features (ManyToMany)
    if 'features' in request.data:
        business.features.set(request.data['features'])

    # Manejar tags (ManyToMany)
    if 'tags' in request.data:
        business.tags.set(request.data['tags'])

    try:
        business.save()
        return Response({
            'success': True,
            'message': 'Negocio actualizado exitosamente',
            'business': BusinessDetailSerializer(business).data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


# ==================== GEOCODIFICACIÓN ====================


@api_view(['POST'])
def geocode_address(request):
    """
    Geocodificar una dirección usando Mapbox API

    Endpoint público que convierte una dirección de texto a coordenadas geográficas.
    Útil para validar direcciones antes de crear/editar negocios.

    POST /api/businesses/geocode/
    Body:
    {
        "address": "Lastarria 305",
        "comuna": "Santiago Centro",  // opcional
        "city": "Santiago, Chile"      // opcional, default: "Santiago, Chile"
    }

    Response (200 OK):
    {
        "success": true,
        "data": {
            "latitude": -33.437198,
            "longitude": -70.638956,
            "formatted_address": "Lastarria 305, Santiago Centro, Santiago, Chile",
            "neighborhood": "Lastarria",
            "comuna": "Santiago Centro",
            "city": "Santiago",
            "country": "Chile",
            "confidence": 0.95
        }
    }

    Response (400 Bad Request):
    {
        "success": false,
        "error": "No se pudo geocodificar la dirección: ..."
    }
    """
    from .services.geocoding_service import GeocodingService, GeocodingError
    from .validators import BusinessLocationValidator

    address = request.data.get('address')
    comuna = request.data.get('comuna')
    city = request.data.get('city', 'Santiago, Chile')

    if not address:
        return Response({
            'success': False,
            'error': 'El campo "address" es requerido'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Preparar dirección completa para geocodificación
        full_address = BusinessLocationValidator.prepare_for_geocoding(address, comuna)

        # Geocodificar usando el servicio
        service = GeocodingService()
        result = service.geocode_address(full_address, city=city)

        return Response({
            'success': True,
            'data': result.to_dict()
        }, status=status.HTTP_200_OK)

    except GeocodingError as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Log error para debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error inesperado en geocode_address: {str(e)}", exc_info=True)

        return Response({
            'success': False,
            'error': 'Error interno al geocodificar la dirección. Por favor intenta nuevamente.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def reverse_geocode(request):
    """
    Reverse geocoding: Obtener dirección desde coordenadas

    Endpoint público que convierte coordenadas a dirección.
    Útil para cuando el usuario selecciona una ubicación en el mapa.

    POST /api/businesses/reverse-geocode/
    Body:
    {
        "latitude": -33.437198,
        "longitude": -70.638956
    }

    Response (200 OK):
    {
        "success": true,
        "data": {
            "latitude": -33.437198,
            "longitude": -70.638956,
            "formatted_address": "Lastarria 305, Santiago Centro, Santiago, Chile",
            "neighborhood": "Lastarria",
            "comuna": "Santiago Centro",
            "city": "Santiago",
            "country": "Chile",
            "confidence": 0.95
        }
    }

    Response (400 Bad Request):
    {
        "success": false,
        "error": "Coordenadas inválidas"
    }
    """
    from .services.geocoding_service import GeocodingService, GeocodingError
    from .validators import CoordinateValidator
    from django.core.exceptions import ValidationError

    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    if latitude is None or longitude is None:
        return Response({
            'success': False,
            'error': 'Los campos "latitude" y "longitude" son requeridos'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Convertir a float
        lat = float(latitude)
        lng = float(longitude)

        # Validar coordenadas
        CoordinateValidator.validate_coordinates(lat, lng)

        # Reverse geocoding usando el servicio
        service = GeocodingService()
        result = service.reverse_geocode(lat, lng)

        return Response({
            'success': True,
            'data': result.to_dict()
        }, status=status.HTTP_200_OK)

    except (ValueError, TypeError):
        return Response({
            'success': False,
            'error': 'Las coordenadas deben ser números válidos'
        }, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except GeocodingError as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Log error para debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error inesperado en reverse_geocode: {str(e)}", exc_info=True)

        return Response({
            'success': False,
            'error': 'Error interno al obtener la dirección. Por favor intenta nuevamente.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== ANALYTICS ENDPOINTS ====================

@api_view(['POST'])
@permission_classes([AllowAny])
def track_business_view(request, business_id):
    """Track view of a business profile (anonymous)"""
    from .models import BusinessView
    
    try:
        business = Business.objects.get(id=business_id, is_active=True)
    except Business.DoesNotExist:
        return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
    
    # Create view record
    BusinessView.objects.create(
        business=business,
        session_key=request.session.session_key if hasattr(request, 'session') else None,
        ip_address=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip(),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
    )
    
    # Update total views counter
    Business.objects.filter(id=business_id).update(views=models.F('views') + 1)
    
    return Response({'success': True, 'message': 'View tracked'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_business_analytics(request, business_id):
    """Get analytics data for business dashboard"""
    from .models import BusinessView, Favorite
    from apps.reviews.models import Review
    from django.db.models import Count
    from django.db.models.functions import TruncDate
    from datetime import datetime, timedelta
    
    try:
        business = Business.objects.get(id=business_id, owner=request.user)
    except Business.DoesNotExist:
        return Response({'error': 'Negocio no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    # Date range (last 7 days)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)
    
    # Views per day
    views_by_day = (
        BusinessView.objects
        .filter(business=business, viewed_at__date__gte=start_date)
        .annotate(date=TruncDate('viewed_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    
    # Favorites per day
    favorites_by_day = (
        Favorite.objects
        .filter(business=business, created_at__date__gte=start_date)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    
    # Reviews per day
    reviews_by_day = (
        Review.objects
        .filter(business=business, created_at__date__gte=start_date, is_approved=True)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    
    # Rating distribution
    rating_distribution = (
        Review.objects
        .filter(business=business, is_approved=True)
        .values('rating')
        .annotate(count=Count('id'))
        .order_by('-rating')
    )
    
    # Build daily data for chart
    daily_data = []
    days_es = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
    
    views_dict = {v['date']: v['count'] for v in views_by_day}
    favorites_dict = {f['date']: f['count'] for f in favorites_by_day}
    reviews_dict = {r['date']: r['count'] for r in reviews_by_day}
    
    for i in range(7):
        day = start_date + timedelta(days=i)
        daily_data.append({
            'date': day.isoformat(),
            'day': days_es[day.weekday()],
            'views': views_dict.get(day, 0),
            'likes': favorites_dict.get(day, 0),
            'reviews': reviews_dict.get(day, 0),
        })
    
    # Rating distribution formatted
    rating_dist = {str(i): 0 for i in range(1, 6)}
    for r in rating_distribution:
        rating_dist[str(r['rating'])] = r['count']
    
    return Response({
        'success': True,
        'data': {
            'daily_activity': daily_data,
            'rating_distribution': rating_dist,
            'totals': {
                'views': business.views,
                'favorites': business.favorites_count,
                'reviews': business.review_count,
                'rating': float(business.rating),
            }
        }
    })
