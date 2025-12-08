from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User"""
    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    emailVerified = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'name', 'role', 'emailVerified',
            'first_name', 'last_name', 'phone', 'avatar',
            'preferred_language', 'notifications_enabled',
            'routes_created', 'businesses_visited', 'created_at'
        )
        read_only_fields = ('id', 'name', 'role', 'emailVerified', 'routes_created', 'businesses_visited', 'created_at')

    def get_name(self, obj):
        """Combina first_name y last_name en un solo campo name"""
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        elif obj.first_name:
            return obj.first_name
        elif obj.last_name:
            return obj.last_name
        return obj.username

    def get_role(self, obj):
        """Devuelve el rol del usuario"""
        if obj.is_superuser:
            return 'admin'
        elif obj.is_staff:
            return 'staff'
        return 'user'

    def get_emailVerified(self, obj):
        """Devuelve si el email está verificado (por ahora siempre True)"""
        return True


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
