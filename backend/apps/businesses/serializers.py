from rest_framework import serializers
from .models import Business, Category, Feature, Tag, Favorite, Visit, BusinessOwnerProfile
from math import radians, sin, cos, sqrt, atan2


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para categorías"""
    business_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'color', 'description', 'business_count']
    
    def get_business_count(self, obj):
        return obj.businesses.filter(is_active=True).count()


class FeatureSerializer(serializers.ModelSerializer):
    """Serializer para features"""
    class Meta:
        model = Feature
        fields = ['id', 'name', 'slug', 'icon', 'category']


class TagSerializer(serializers.ModelSerializer):
    """Serializer para tags"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class BusinessListSerializer(serializers.ModelSerializer):
    """Serializer para listado de negocios (versión simplificada)"""
    category = CategorySerializer(read_only=True)
    location = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()
    closes_at = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'slug', 'short_description', 'category', 'location',
            'address', 'neighborhood', 'rating', 'review_count', 'price_range',
            'distance', 'cover_image', 'features', 'is_open', 'closes_at', 'verified'
        ]
    
    def get_location(self, obj):
        return {
            'lat': float(obj.latitude),
            'lng': float(obj.longitude)
        }
    
    def get_features(self, obj):
        # Solo retornar nombres de features para el listado
        return [f.name for f in obj.features.all()[:5]]
    
    def get_distance(self, obj):
        """Calcular distancia si se proporciona lat/lng en el contexto"""
        user_lat = self.context.get('user_lat')
        user_lng = self.context.get('user_lng')
        
        if user_lat and user_lng:
            # Fórmula de Haversine para calcular distancia
            R = 6371  # Radio de la Tierra en km
            
            lat1 = radians(float(user_lat))
            lon1 = radians(float(user_lng))
            lat2 = radians(float(obj.latitude))
            lon2 = radians(float(obj.longitude))
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            
            distance = R * c
            return round(distance, 2)
        
        return None
    
    def get_is_open(self, obj):
        """Verificar si el negocio está abierto actualmente"""
        # TODO: Implementar lógica de horarios
        return True
    
    def get_closes_at(self, obj):
        """Obtener hora de cierre"""
        # TODO: Implementar lógica de horarios
        return "22:00"


class BusinessDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para un negocio"""
    category = CategorySerializer(read_only=True)
    features = FeatureSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    location = serializers.SerializerMethodField()
    recent_reviews = serializers.SerializerMethodField()
    similar_businesses = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'slug', 'description', 'short_description', 'category',
            'subcategory', 'tags', 'location', 'address', 'neighborhood', 'comuna',
            'phone', 'email', 'website', 'instagram', 'hours', 'is_open_24h',
            'features', 'price_range', 'rating', 'review_count', 'images',
            'cover_image', 'logo', 'verified', 'views', 'favorites_count',
            'recent_reviews', 'similar_businesses', 'created_at'
        ]
    
    def get_location(self, obj):
        return {
            'lat': float(obj.latitude),
            'lng': float(obj.longitude)
        }
    
    def get_recent_reviews(self, obj):
        """Obtener 3 reseñas más recientes"""
        from apps.reviews.models import Review
        from apps.reviews.serializers import ReviewSerializer
        
        reviews = Review.objects.filter(
            business=obj,
            is_approved=True
        ).select_related('user')[:3]
        
        return ReviewSerializer(reviews, many=True).data
    
    def get_similar_businesses(self, obj):
        """Obtener negocios similares"""
        similar = Business.objects.filter(
            category=obj.category,
            is_active=True
        ).exclude(id=obj.id)[:4]
        
        return BusinessListSerializer(similar, many=True, context=self.context).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer para favoritos"""
    business = BusinessListSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'business', 'created_at']


class VisitSerializer(serializers.ModelSerializer):
    """Serializer para visitas"""
    business = BusinessListSerializer(read_only=True)
    
    class Meta:
        model = Visit
        fields = ['id', 'business', 'route', 'visited_at', 'notes']
        read_only_fields = ['id', 'visited_at']


class BusinessOwnerProfileSerializer(serializers.ModelSerializer):
    businesses_created_count = serializers.IntegerField(read_only=True)
    can_create_more = serializers.BooleanField(read_only=True)
    remaining_slots = serializers.ReadOnlyField()
    
    class Meta:
        model = BusinessOwnerProfile
        fields = [
            'can_create_businesses',
            'max_businesses_allowed',
            'businesses_created_count',
            'can_create_more',
            'remaining_slots',
            'is_verified_owner'
        ]


class BusinessCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            'name', 'description', 'short_description', 'category',
            'latitude', 'longitude', 'address', 'neighborhood', 'comuna',
            'phone', 'email', 'website', 'instagram',
            'cover_image', 'images', 'hours', 'price_range', 'features', 'tags'
        ]
    
    def create(self, validated_data):
        # Extraer ManyToMany antes de crear
        features = validated_data.pop('features', [])
        tags = validated_data.pop('tags', [])
        
        # Crear negocio
        business = Business.objects.create(
            **validated_data,
            owner=self.context['request'].user,
            created_by_owner=True,
            status='pending_review'
        )
        
        # Agregar relaciones
        business.features.set(features)
        business.tags.set(tags)
        
        return business
