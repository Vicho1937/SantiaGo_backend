"""
Script para crear superusuario automáticamente
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Credenciales del superusuario
username = 'admin'
email = 'admin@rutalocal.com'
password = 'admin123'

# Verificar si ya existe
if User.objects.filter(username=username).exists():
    print(f"⚠️  El usuario '{username}' ya existe!")
    user = User.objects.get(username=username)
    print(f"📧 Email: {user.email}")
else:
    # Crear superusuario
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("✅ ¡Superusuario creado exitosamente!")
    print(f"")
    print(f"📋 Credenciales:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"")
    print(f"🔗 Acceso al Admin Panel:")
    print(f"   http://localhost:8000/admin")
    print(f"")
    print(f"⚠️  IMPORTANTE: Cambia la contraseña en producción!")
