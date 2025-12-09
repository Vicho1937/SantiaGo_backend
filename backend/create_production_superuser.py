"""
Script para crear superusuario en producción usando variables de entorno
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Obtener credenciales de variables de entorno
email = os.environ.get('SUPERUSER_EMAIL')
password = os.environ.get('SUPERUSER_PASSWORD')
username = os.environ.get('SUPERUSER_USERNAME', 'admin')

if not email or not password:
    print("❌ ERROR: Debes configurar las variables de entorno:")
    print("   - SUPERUSER_EMAIL")
    print("   - SUPERUSER_PASSWORD")
    print("   - SUPERUSER_USERNAME (opcional, default: admin)")
    exit(1)

# Verificar si ya existe
if User.objects.filter(email=email).exists():
    print(f"⚠️  Ya existe un usuario con el email: {email}")
    user = User.objects.get(email=email)
    print(f"   Username: {user.username}")
    print(f"   Is superuser: {user.is_superuser}")
    print(f"   Is staff: {user.is_staff}")
    
    # Actualizar si no es superuser
    if not user.is_superuser:
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print("✅ Usuario actualizado a superuser!")
else:
    # Crear superusuario
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name='Admin',
        last_name='RutaGO'
    )
    print("✅ ¡Superusuario creado exitosamente!")
    print(f"")
    print(f"📋 Información:")
    print(f"   Email: {email}")
    print(f"   Username: {username}")
    print(f"")
    print(f"🔗 Acceso al Admin Panel:")
    print(f"   https://web-production-f3cae.up.railway.app/admin/")
    print(f"")
    print(f"✅ Inicia sesión con tu email y contraseña")
