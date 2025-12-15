"""
Management command para geocodificar negocios existentes

Geocodifica todos los negocios que:
1. No tienen coordenadas válidas
2. Tienen coordenadas por defecto del centro de Santiago
3. Tienen coordenadas pero están muy cerca del centro (posiblemente defaults)

Uso:
    python manage.py geocode_existing_businesses
    python manage.py geocode_existing_businesses --dry-run
    python manage.py geocode_existing_businesses --force-all

Autor: Senior Developer
Fecha: 2025-12-15
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.businesses.models import Business
from apps.businesses.services.geocoding_service import GeocodingService, GeocodingError
from apps.businesses.validators import AddressValidator, BusinessLocationValidator
from decimal import Decimal
import time


class Command(BaseCommand):
    help = 'Geocodifica negocios existentes que no tienen coordenadas correctas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra qué se haría sin hacer cambios reales',
        )
        parser.add_argument(
            '--force-all',
            action='store_true',
            help='Geocodifica todos los negocios, incluso los que ya tienen coordenadas',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=10,
            help='Número de negocios a procesar en cada lote (default: 10)',
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=0.2,
            help='Delay en segundos entre geocodificaciones para no saturar la API (default: 0.2)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force_all = options['force_all']
        batch_size = options['batch_size']
        delay = options['delay']

        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('🗺️  GEOCODIFICACIÓN DE NEGOCIOS EXISTENTES'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write()

        if dry_run:
            self.stdout.write(self.style.WARNING('⚠️  Modo DRY RUN - No se harán cambios reales'))
            self.stdout.write()

        # Coordenadas del centro de Santiago (defaults comunes)
        SANTIAGO_CENTER_LAT = Decimal('-33.4372')
        SANTIAGO_CENTER_LNG = Decimal('-70.6506')
        TOLERANCE = Decimal('0.01')  # ~1km de tolerancia

        # Filtrar negocios que necesitan geocodificación
        all_businesses = Business.objects.filter(is_active=True)

        if force_all:
            businesses_to_geocode = all_businesses
            self.stdout.write(f"📊 Modo FORCE-ALL: Geocodificando {businesses_to_geocode.count()} negocios")
        else:
            # Solo negocios que probablemente tienen coordenadas incorrectas
            businesses_to_geocode = []

            for business in all_businesses:
                needs_geocoding = False
                reason = ""

                # Caso 1: Sin coordenadas
                if not business.latitude or not business.longitude:
                    needs_geocoding = True
                    reason = "Sin coordenadas"
                # Caso 2: Coordenadas por defecto del centro
                elif (abs(business.latitude - SANTIAGO_CENTER_LAT) < TOLERANCE and
                      abs(business.longitude - SANTIAGO_CENTER_LNG) < TOLERANCE):
                    needs_geocoding = True
                    reason = "Coordenadas por defecto (centro de Santiago)"

                if needs_geocoding:
                    businesses_to_geocode.append((business, reason))

            self.stdout.write(f"📊 Negocios que necesitan geocodificación: {len(businesses_to_geocode)}")
            self.stdout.write(f"📊 Negocios totales: {all_businesses.count()}")

        self.stdout.write()

        if not businesses_to_geocode:
            self.stdout.write(self.style.SUCCESS('✅ Todos los negocios ya tienen coordenadas correctas'))
            return

        # Inicializar servicio de geocodificación
        geocoding_service = GeocodingService()

        # Estadísticas
        stats = {
            'total': len(businesses_to_geocode) if isinstance(businesses_to_geocode, list) else businesses_to_geocode.count(),
            'success': 0,
            'failed': 0,
            'skipped': 0
        }

        # Procesar negocios
        for i, item in enumerate(businesses_to_geocode, 1):
            if isinstance(item, tuple):
                business, reason = item
            else:
                business = item
                reason = "Forzado"

            self.stdout.write(f"\n[{i}/{stats['total']}] {business.name}")
            self.stdout.write(f"  📍 Dirección: {business.address}")
            self.stdout.write(f"  ℹ️  Razón: {reason}")

            if not business.address:
                self.stdout.write(self.style.ERROR('  ❌ Sin dirección - OMITIDO'))
                stats['skipped'] += 1
                continue

            # Preparar dirección completa
            full_address = BusinessLocationValidator.prepare_for_geocoding(
                business.address,
                business.comuna
            )

            try:
                # Geocodificar
                self.stdout.write(f"  🔍 Geocodificando: {full_address}")
                result = geocoding_service.geocode_address(full_address)

                self.stdout.write(self.style.SUCCESS(f"  ✓ Encontrado: {result.formatted_address}"))
                self.stdout.write(f"  📌 Coordenadas: {result.latitude}, {result.longitude}")

                if not dry_run:
                    # Actualizar negocio
                    business.latitude = result.latitude
                    business.longitude = result.longitude
                    business.address = result.formatted_address

                    if result.neighborhood and not business.neighborhood:
                        business.neighborhood = result.neighborhood
                    if result.comuna and not business.comuna:
                        business.comuna = result.comuna

                    business.save()
                    self.stdout.write(self.style.SUCCESS('  💾 Guardado en base de datos'))
                else:
                    self.stdout.write(self.style.WARNING('  🔄 No guardado (dry-run)'))

                stats['success'] += 1

                # Delay para no saturar la API
                if delay > 0 and i < stats['total']:
                    time.sleep(delay)

            except GeocodingError as e:
                self.stdout.write(self.style.ERROR(f'  ❌ Error de geocodificación: {str(e)}'))
                stats['failed'] += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ❌ Error inesperado: {str(e)}'))
                stats['failed'] += 1

        # Resumen final
        self.stdout.write()
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('📊 RESUMEN DE GEOCODIFICACIÓN'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(f"Total procesados:  {stats['total']}")
        self.stdout.write(self.style.SUCCESS(f"✅ Exitosos:       {stats['success']}"))
        self.stdout.write(self.style.ERROR(f"❌ Fallidos:       {stats['failed']}"))
        self.stdout.write(self.style.WARNING(f"⏭️  Omitidos:       {stats['skipped']}"))
        self.stdout.write()

        if dry_run:
            self.stdout.write(self.style.WARNING('⚠️  DRY RUN - No se hicieron cambios reales'))
            self.stdout.write(self.style.WARNING('   Ejecuta sin --dry-run para aplicar los cambios'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Geocodificación completada'))
            self.stdout.write()
            self.stdout.write('💡 Los negocios actualizados ahora deberían aparecer correctamente en el mapa')

        self.stdout.write(self.style.SUCCESS('=' * 70))
