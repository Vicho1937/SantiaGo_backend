#!/usr/bin/env python
"""
Script para probar el login JWT
Uso: python test_login.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.authentication.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def test_login():
    """Prueba el login y genera tokens JWT"""

    print("🔐 Script de prueba de login JWT")
    print("=" * 50)
    print()

    # Solicitar credenciales
    print("Ingresa tus credenciales:")
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    print()

    # Autenticar
    from django.contrib.auth import authenticate
    user = authenticate(username=email, password=password)

    if not user:
        print("❌ Credenciales incorrectas")
        print()
        print("💡 Verifica que:")
        print("   - El email sea correcto")
        print("   - La contraseña sea correcta")
        print("   - El usuario exista en la base de datos")
        print()
        print("📋 Superusuarios disponibles:")
        for u in User.objects.filter(is_superuser=True):
            print(f"   - {u.email} (username: {u.username})")
        return

    print("✅ Login exitoso!")
    print()
    print(f"👤 Usuario autenticado:")
    print(f"   Email: {user.email}")
    print(f"   Username: {user.username}")
    print(f"   Name: {user.first_name} {user.last_name}")
    print(f"   Is superuser: {user.is_superuser}")
    print(f"   Is staff: {user.is_staff}")
    print()

    # Generar tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    print("🎟️  Tokens JWT generados:")
    print()
    print("Access Token (válido por 60 minutos):")
    print(f"   {access_token[:50]}...")
    print()
    print("Refresh Token (válido por 7 días):")
    print(f"   {refresh_token[:50]}...")
    print()

    # Mostrar ejemplos de uso
    print("=" * 50)
    print("📝 Ejemplos de uso:")
    print()
    print("1. Probar el endpoint /api/ (ahora protegido):")
    print(f"""
curl https://web-production-f3cae.up.railway.app/api/ \\
  -H "Authorization: Bearer {access_token[:30]}..."
""")

    print("2. Ver tu perfil (/api/auth/me/):")
    print(f"""
curl https://web-production-f3cae.up.railway.app/api/auth/me/ \\
  -H "Authorization: Bearer {access_token[:30]}..."
""")

    print("3. Crear una ruta:")
    print(f"""
curl -X POST https://web-production-f3cae.up.railway.app/api/routes/create/ \\
  -H "Authorization: Bearer {access_token[:30]}..." \\
  -H "Content-Type: application/json" \\
  -d '{{"name": "Mi Ruta", "description": "Test", "is_public": true, "stops": []}}'
""")

    print()
    print("=" * 50)
    print("✅ Script completado exitosamente")

if __name__ == '__main__':
    test_login()
