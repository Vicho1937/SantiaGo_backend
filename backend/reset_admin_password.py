#!/usr/bin/env python
"""
Script para resetear la contraseña del superusuario AdminRutaGo
Uso: python reset_admin_password.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.authentication.models import User

def reset_admin_password():
    """Resetea la contraseña del superusuario AdminRutaGo"""

    print("🔧 Script para resetear contraseña del superusuario")
    print("=" * 50)

    try:
        # Buscar el superusuario
        user = User.objects.get(username='AdminRutaGo')

        print(f"✅ Usuario encontrado:")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Is superuser: {user.is_superuser}")
        print(f"   Is staff: {user.is_staff}")
        print()

        # Solicitar nueva contraseña
        print("🔑 Ingresa la nueva contraseña:")
        new_password = input("   Password: ")

        if len(new_password) < 8:
            print("❌ La contraseña debe tener al menos 8 caracteres")
            return

        # Confirmar contraseña
        print("🔑 Confirma la nueva contraseña:")
        confirm_password = input("   Password: ")

        if new_password != confirm_password:
            print("❌ Las contraseñas no coinciden")
            return

        # Actualizar contraseña
        user.set_password(new_password)
        user.save()

        print()
        print("✅ Contraseña actualizada exitosamente!")
        print()
        print("📝 Nuevas credenciales:")
        print(f"   Email: {user.email}")
        print(f"   Username: {user.username}")
        print(f"   Password: {new_password}")
        print()
        print("🔐 Puedes usar estas credenciales para:")
        print("   - Login en /api/auth/login/")
        print("   - Django Admin en /admin/")
        print("   - DRF Browsable API en /api-auth/login/")
        print()

        # Probar el login
        print("🧪 Probando credenciales...")
        from django.contrib.auth import authenticate
        auth_user = authenticate(username=user.email, password=new_password)

        if auth_user:
            print("✅ Credenciales verificadas correctamente")
        else:
            print("⚠️  Error al verificar credenciales")

    except User.DoesNotExist:
        print("❌ No se encontró el usuario 'AdminRutaGo'")
        print()
        print("📋 Usuarios disponibles:")
        for u in User.objects.filter(is_superuser=True):
            print(f"   - {u.username} ({u.email})")

if __name__ == '__main__':
    reset_admin_password()
