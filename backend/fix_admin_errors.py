"""
Script para aplicar las correcciones de base de datos necesarias para el panel de admin.
Resuelve los errores 500 en las secciones:
- Favorites
- Negocios  
- Perfiles de propietarios
- Visits
- Reviews
- Paradas de rutas
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

django.setup()

from django.db import connection
from django.core.management import call_command


def apply_sql_fix():
    """Aplica el script SQL de corrección"""
    print("🔧 Aplicando correcciones a la base de datos...")
    
    sql_file = BASE_DIR / 'fix_database.sql'
    
    if not sql_file.exists():
        print("❌ No se encontró el archivo fix_database.sql")
        return False
    
    with open(sql_file, 'r') as f:
        sql_script = f.read()
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_script)
        print("✅ Script SQL aplicado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al aplicar el script SQL: {e}")
        return False


def run_migrations():
    """Ejecuta las migraciones de Django"""
    print("\n📦 Aplicando migraciones de Django...")
    
    try:
        call_command('migrate', '--noinput')
        print("✅ Migraciones aplicadas correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al aplicar migraciones: {e}")
        return False


def verify_tables():
    """Verifica que las tablas y columnas necesarias existan"""
    print("\n🔍 Verificando estructura de la base de datos...")
    
    checks = []
    
    with connection.cursor() as cursor:
        # Verificar columnas en businesses
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'businesses' 
            AND column_name IN ('created_by_owner', 'status', 'approved_by_id', 'approved_at', 'rejection_reason')
        """)
        businesses_columns = [row[0] for row in cursor.fetchall()]
        
        required_columns = ['created_by_owner', 'status', 'approved_by_id', 'approved_at', 'rejection_reason']
        for col in required_columns:
            if col in businesses_columns:
                print(f"✅ Columna businesses.{col} existe")
                checks.append(True)
            else:
                print(f"❌ Columna businesses.{col} NO existe")
                checks.append(False)
        
        # Verificar tabla business_owner_profiles
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'business_owner_profiles'
            )
        """)
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            print("✅ Tabla business_owner_profiles existe")
            checks.append(True)
        else:
            print("❌ Tabla business_owner_profiles NO existe")
            checks.append(False)
    
    return all(checks)


def main():
    """Función principal"""
    print("🚀 Iniciando corrección de base de datos para Django Admin\n")
    print("=" * 60)
    
    # Paso 1: Aplicar SQL
    if not apply_sql_fix():
        print("\n⚠️  Intentando con migraciones de Django...")
        if not run_migrations():
            print("\n❌ No se pudieron aplicar las correcciones")
            sys.exit(1)
    
    # Paso 2: Ejecutar migraciones
    if not run_migrations():
        print("\n⚠️  Advertencia: Algunas migraciones fallaron")
    
    # Paso 3: Verificar
    print()
    if verify_tables():
        print("\n" + "=" * 60)
        print("✅ ¡Correcciones aplicadas exitosamente!")
        print("=" * 60)
        print("\n📝 Ahora deberías poder acceder a todas las secciones del admin:")
        print("   - Favorites")
        print("   - Negocios")
        print("   - Perfiles de propietarios ⭐")
        print("   - Visits")
        print("   - Reviews")
        print("   - Paradas de rutas")
        print("\n🔗 Reinicia el servidor para ver los cambios")
    else:
        print("\n" + "=" * 60)
        print("⚠️  Algunas verificaciones fallaron")
        print("=" * 60)
        print("\n📋 Revisa los logs arriba para ver qué falta")
        sys.exit(1)


if __name__ == '__main__':
    main()
