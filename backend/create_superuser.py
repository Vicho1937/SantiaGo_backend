"""
Script para crear superusuario automáticamente desde variables de entorno
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Credenciales desde variables de entorno
username = os.environ.get('SUPERUSER_USERNAME', 'admin')
email = os.environ.get('SUPERUSER_EMAIL', 'admin@rutalocal.com')
password = os.environ.get('SUPERUSER_PASSWORD', 'admin123')

print("🔧 Iniciando creación de superusuario...")
print(f"📋 Username: {username}")
print(f"📧 Email: {email}")
print("")

# Verificar si ya existe
if User.objects.filter(username=username).exists():
    print(f"⚠️  El usuario '{username}' ya existe!")
    user = User.objects.get(username=username)
    print(f"📧 Email actual: {user.email}")
    print(f"✅ Superusuario ya está disponible")
elif User.objects.filter(email=email).exists():
    print(f"⚠️  Ya existe un usuario con el email '{email}'")
    user = User.objects.get(email=email)
    print(f"👤 Username: {user.username}")
    print(f"✅ Superusuario ya está disponible")
else:
    # Crear superusuario
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("✅ ¡Superusuario creado exitosamente!")
        print(f"")
        print(f"📋 Credenciales configuradas:")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {'*' * len(password)}")
        print(f"")
        print(f"🔗 Puedes acceder al Admin Panel en:")
        print(f"   /admin/")
        print(f"")
    except Exception as e:
        print(f"❌ Error al crear superusuario: {e}")
        exit(1)
