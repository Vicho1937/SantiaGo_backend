"""
Script para probar la conexión a la base de datos
Ejecutar: python test_connection.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.db import connection

print("🔍 Probando conexión a la base de datos...")
print("=" * 60)

try:
    # Intentar conectar
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print("✅ Conexión exitosa!")
        print(f"📊 Versión de PostgreSQL: {db_version[0]}")
        print("=" * 60)
        
        # Probar que podemos crear tablas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            LIMIT 5;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print("\n📋 Tablas existentes:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("\n📋 No hay tablas aún (esto es normal en una BD nueva)")
        
        print("\n🎉 ¡Todo listo! Puedes ejecutar las migraciones:")
        print("   python manage.py migrate")
        
except Exception as e:
    print("❌ Error de conexión:")
    print(f"   {e}")
    print("\n💡 Verifica:")
    print("   1. Las credenciales en el archivo .env")
    print("   2. Que la contraseña sea la correcta")
    print("   3. Que Supabase esté accesible")
