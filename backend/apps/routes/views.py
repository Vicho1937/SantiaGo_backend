from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db import models
from .models import Route, RouteLike
from .serializers import (
    RouteListSerializer, RouteDetailSerializer,
    RouteCreateSerializer, RouteUpdateSerializer
)


class RouteListView(generics.ListAPIView):
    """Listar rutas del usuario autenticado"""
    serializer_class = RouteListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Route.objects.filter(user=self.request.user).prefetch_related('stops__business')
        
        # Filtro por visibilidad
        is_public = self.request.query_params.get('is_public')
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public.lower() == 'true')
        
        return queryset
    
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


class RouteDetailView(generics.RetrieveAPIView):
    """Detalle de una ruta"""
    serializer_class = RouteDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    
    def get_queryset(self):
        # Mostrar rutas públicas o propias
        if self.request.user.is_authenticated:
            return Route.objects.filter(
                models.Q(is_public=True) | models.Q(user=self.request.user)
            ).select_related('user').prefetch_related('stops__business')
        return Route.objects.filter(is_public=True).select_related('user').prefetch_related('stops__business')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Incrementar contador de vistas
        Route.objects.filter(id=instance.id).update(views=models.F('views') + 1)
        
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data
        })


class RouteCreateView(generics.CreateAPIView):
    """Crear nueva ruta"""
    serializer_class = RouteCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            route = serializer.save()
            return Response({
                'success': True,
                'data': RouteDetailSerializer(route).data,
                'message': 'Ruta creada exitosamente'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Error en la validación'
        }, status=status.HTTP_400_BAD_REQUEST)


class RouteUpdateView(generics.UpdateAPIView):
    """Actualizar ruta"""
    serializer_class = RouteUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Route.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            route = serializer.save()
            return Response({
                'success': True,
                'data': RouteDetailSerializer(route).data,
                'message': 'Ruta actualizada exitosamente'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Error en la validación'
        }, status=status.HTTP_400_BAD_REQUEST)


class RouteDeleteView(generics.DestroyAPIView):
    """Eliminar ruta"""
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Route.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Decrementar contador de rutas del usuario
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.filter(id=request.user.id).update(routes_created=models.F('routes_created') - 1)
        
        instance.delete()
        
        return Response({
            'success': True,
            'message': 'Ruta eliminada exitosamente'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_route(request, route_id):
    """Dar like a una ruta"""
    try:
        route = Route.objects.get(id=route_id, is_public=True)
    except Route.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Ruta no encontrada'
        }, status=status.HTTP_404_NOT_FOUND)
    
    like, created = RouteLike.objects.get_or_create(
        route=route,
        user=request.user
    )
    
    if created:
        # Incrementar contador
        Route.objects.filter(id=route_id).update(likes=models.F('likes') + 1)
        
        return Response({
            'success': True,
            'message': 'Like agregado'
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': True,
        'message': 'Ya has dado like a esta ruta'
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike_route(request, route_id):
    """Quitar like de una ruta"""
    try:
        like = RouteLike.objects.get(route_id=route_id, user=request.user)
        like.delete()
        
        # Decrementar contador
        Route.objects.filter(id=route_id).update(likes=models.F('likes') - 1)
        
        return Response({
            'success': True,
            'message': 'Like eliminado'
        }, status=status.HTTP_200_OK)
    
    except RouteLike.DoesNotExist:
        return Response({
            'success': False,
            'message': 'No has dado like a esta ruta'
        }, status=status.HTTP_404_NOT_FOUND)
