from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.businesses.models import Business, BusinessOwnerProfile


class Command(BaseCommand):
    """
    Comando para publicar automáticamente los negocios pendientes
    que pertenecen a usuarios con permisos aprobados.

    Este comando soluciona el problema de negocios que fueron creados
    antes de implementar la lógica de auto-publicación para usuarios verificados.

    Uso:
        python manage.py publish_approved_businesses
        python manage.py publish_approved_businesses --dry-run  # Solo mostrar sin actualizar
    """
    help = 'Publica negocios pendientes de usuarios con permisos aprobados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar negocios a publicar sin actualizar la base de datos',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        self.stdout.write(self.style.WARNING('Buscando negocios pendientes de usuarios con permisos...'))

        # Obtener todos los perfiles de propietarios con permisos activos
        approved_profiles = BusinessOwnerProfile.objects.filter(can_create_businesses=True)
        approved_user_ids = approved_profiles.values_list('user_id', flat=True)

        # Buscar negocios pendientes de estos usuarios
        pending_businesses = Business.objects.filter(
            status='pending_review',
            created_by_owner=True,
            owner_id__in=approved_user_ids,
            is_active=True
        ).select_related('owner')

        total_count = pending_businesses.count()

        if total_count == 0:
            self.stdout.write(self.style.SUCCESS('✓ No se encontraron negocios pendientes de usuarios aprobados.'))
            return

        self.stdout.write(self.style.WARNING(f'\nSe encontraron {total_count} negocios para publicar:\n'))

        # Mostrar detalles
        for business in pending_businesses:
            self.stdout.write(
                f'  - {business.name} (ID: {business.id})'
                f'\n    Propietario: {business.owner.email}'
                f'\n    Creado: {business.created_at.strftime("%Y-%m-%d %H:%M")}\n'
            )

        if dry_run:
            self.stdout.write(self.style.WARNING('\n[DRY RUN] No se realizaron cambios. Ejecuta sin --dry-run para aplicar.'))
            return

        # Confirmar acción
        self.stdout.write(self.style.WARNING(f'\n¿Deseas publicar estos {total_count} negocios? [y/N]: '), ending='')
        confirm = input().strip().lower()

        if confirm != 'y':
            self.stdout.write(self.style.ERROR('Operación cancelada.'))
            return

        # Actualizar negocios
        updated_count = pending_businesses.update(
            status='published',
            approved_at=timezone.now()
        )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ {updated_count} negocios publicados exitosamente!')
        )
        self.stdout.write(
            self.style.SUCCESS('Estos negocios ahora son visibles en búsquedas, filtros y destacados.')
        )
