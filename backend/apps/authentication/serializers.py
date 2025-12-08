from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User"""
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone', 'avatar', 'preferred_language', 'notifications_enabled',
            'routes_created', 'businesses_visited', 'created_at'
        )
        read_only_fields = ('id', 'routes_created', 'businesses_visited', 'created_at')


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de usuarios"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_confirmation', 'first_name', 'last_name')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            
            if not user:
                raise serializers.ValidationError("Credenciales inválidas.")
            
            if not user.is_active:
                raise serializers.ValidationError("Esta cuenta está desactivada.")
        else:
            raise serializers.ValidationError("Debe incluir email y contraseña.")
        
        attrs['user'] = user
        return attrs


class GoogleAuthSerializer(serializers.Serializer):
    """Serializer para autenticación con Google"""
    token = serializers.CharField(required=True)
