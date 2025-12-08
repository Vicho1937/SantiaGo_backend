from rest_framework import serializers
from .models import Route, RouteStop
from apps.businesses.serializers import BusinessListSerializer
from apps.authentication.serializers import UserSerializer


class RouteStopSerializer(serializers.ModelSerializer):
    """Serializer para paradas de ruta"""
    business = BusinessListSerializer(read_only=True)
    business_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = RouteStop
        fields = ['id', 'business', 'business_id', 'order', 'duration', 'notes', 'is_completed', 'completed_at']
        read_only_fields = ['id', 'is_completed', 'completed_at']


class RouteListSerializer(serializers.ModelSerializer):
    """Serializer para listado de rutas (simplificado)"""
    preview_businesses = serializers.SerializerMethodField()
    
    class Meta:
        model = Route
        fields = [
            'id', 'name', 'description', 'stops_count', 'total_distance',
            'estimated_duration', 'is_public', 'likes', 'created_at', 'preview_businesses'
        ]
    
    def get_preview_businesses(self, obj):
        """Obtener primeros 3 negocios de la ruta"""
        stops = obj.stops.all().select_related('business')[:3]
        return [{
            'id': str(stop.business.id),
            'name': stop.business.name,
            'cover_image': stop.business.cover_image
        } for stop in stops]


class RouteDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para una ruta"""
    user = UserSerializer(read_only=True)
    stops = RouteStopSerializer(many=True, read_only=True)
    
    class Meta:
        model = Route
        fields = [
            'id', 'user', 'name', 'description', 'stops', 'total_distance',
            'estimated_duration', 'is_public', 'views', 'likes', 'shares',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'views', 'likes', 'shares', 'created_at', 'updated_at']


class RouteCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear rutas"""
    stops = RouteStopSerializer(many=True)
    
    class Meta:
        model = Route
        fields = ['name', 'description', 'is_public', 'stops']
    
    def validate_stops(self, value):
        """Validar que haya al menos 2 paradas"""
        if len(value) < 2:
            raise serializers.ValidationError("Una ruta debe tener al menos 2 paradas")
        return value
    
    def create(self, validated_data):
        stops_data = validated_data.pop('stops')
        
        # Crear ruta
        route = Route.objects.create(user=self.context['request'].user, **validated_data)
        
        # Crear paradas
        from apps.businesses.models import Business
        for stop_data in stops_data:
            business_id = stop_data.pop('business_id')
            try:
                business = Business.objects.get(id=business_id, is_active=True)
                RouteStop.objects.create(route=route, business=business, **stop_data)
            except Business.DoesNotExist:
                route.delete()
                raise serializers.ValidationError(f"Negocio {business_id} no encontrado")
        
        # Actualizar stats
        route.update_stats()
        
        # Incrementar contador de rutas del usuario
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.filter(id=route.user.id).update(routes_created=models.F('routes_created') + 1)
        
        return route


class RouteUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar rutas"""
    stops = RouteStopSerializer(many=True, required=False)
    
    class Meta:
        model = Route
        fields = ['name', 'description', 'is_public', 'stops']
    
    def update(self, instance, validated_data):
        stops_data = validated_data.pop('stops', None)
        
        # Actualizar campos básicos
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.is_public = validated_data.get('is_public', instance.is_public)
        instance.save()
        
        # Actualizar paradas si se proporcionan
        if stops_data is not None:
            # Eliminar paradas existentes
            instance.stops.all().delete()
            
            # Crear nuevas paradas
            from apps.businesses.models import Business
            for stop_data in stops_data:
                business_id = stop_data.pop('business_id')
                try:
                    business = Business.objects.get(id=business_id, is_active=True)
                    RouteStop.objects.create(route=instance, business=business, **stop_data)
                except Business.DoesNotExist:
                    raise serializers.ValidationError(f"Negocio {business_id} no encontrado")
            
            # Actualizar stats
            instance.update_stats()
        
        return instance


# Import models for F expressions
from django.db import models
