"""
Script de configuración rápida del backend
Ejecutar: python setup.py
"""
import subprocess
import sys
import os


def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(f"⚠️  {result.stderr}")
        print(f"✅ {description} - Completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.output}")
        return False


def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           🚀 RUTA LOCAL - BACKEND SETUP                   ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Verificar si existe .env
    if not os.path.exists('.env'):
        print("\n⚠️  Archivo .env no encontrado.")
        response = input("¿Deseas copiar .env.example a .env? (s/n): ")
        if response.lower() == 's':
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Archivo .env creado. Por favor configura tus variables de entorno.")
            print("   Edita el archivo .env antes de continuar.")
            input("\nPresiona Enter cuando hayas configurado .env...")
        else:
            print("❌ Se necesita un archivo .env para continuar.")
            sys.exit(1)
    
    print("\n📦 Instalando dependencias...")
    
    # 1. Instalar dependencias
    if not run_command(
        "pip install -r requirements/development.txt",
        "Instalando dependencias de Python"
    ):
        print("\n❌ Error instalando dependencias. Verifica que pip esté instalado.")
        sys.exit(1)
    
    # 2. Ejecutar migraciones
    if not run_command(
        "python manage.py migrate",
        "Ejecutando migraciones de base de datos"
    ):
        print("\n⚠️  Error en migraciones. Verifica tu configuración de PostgreSQL.")
        response = input("¿Deseas continuar de todos modos? (s/n): ")
        if response.lower() != 's':
            sys.exit(1)
    
    # 3. Cargar fixtures
    print("\n📊 Cargando datos de ejemplo...")
    run_command(
        "python manage.py loaddata fixtures/categories.json",
        "Cargando categorías"
    )
    run_command(
        "python manage.py loaddata fixtures/features.json",
        "Cargando características"
    )
    
    # 4. Seed businesses
    run_command(
        "python manage.py seed_businesses",
        "Creando negocios de ejemplo"
    )
    
    # 5. Crear superusuario
    print("\n👤 Creación de superusuario")
    response = input("¿Deseas crear un superusuario ahora? (s/n): ")
    if response.lower() == 's':
        run_command(
            "python manage.py createsuperuser",
            "Creando superusuario"
        )
    
    print("""
    
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           ✅ SETUP COMPLETADO EXITOSAMENTE                ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    
    🚀 Para iniciar el servidor de desarrollo:
    
       python manage.py runserver
    
    📱 El servidor estará disponible en:
       http://localhost:8000
    
    🔐 Panel de administración:
       http://localhost:8000/admin
    
    📚 Endpoints API:
       http://localhost:8000/api/
    
    ═══════════════════════════════════════════════════════════
    
    📖 Consulta README_BACKEND.md para más información
    """)


if __name__ == '__main__':
    main()
