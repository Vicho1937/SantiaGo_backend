from rest_framework import serializers
from .models import Review, ReviewHelpful
from apps.authentication.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer para reviews"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'rating', 'title', 'comment', 'would_recommend',
            'images', 'helpful_count', 'is_verified_visit', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'helpful_count', 'is_verified_visit', 'created_at', 'updated_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment', 'would_recommend', 'images']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("El rating debe estar entre 1 y 5")
        return value
    
    def validate(self, attrs):
        # Verificar que el usuario no tenga ya una review para este negocio
        user = self.context['request'].user
        business = self.context['business']
        
        if Review.objects.filter(user=user, business=business).exists():
            raise serializers.ValidationError("Ya has escrito una reseña para este negocio")
        
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['business'] = self.context['business']
        return super().create(validated_data)


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment', 'would_recommend', 'images']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("El rating debe estar entre 1 y 5")
        return value
