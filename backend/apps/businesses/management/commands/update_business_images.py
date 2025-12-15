from django.core.management.base import BaseCommand
from apps.businesses.models import Business


class Command(BaseCommand):
    help = 'Actualizar imágenes de negocios con URLs de alta calidad de Unsplash'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar qué se actualizaría sin modificar la base de datos',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Mapeo de negocios a nuevas imágenes de alta calidad
        image_mapping = {
            'Café Literario': 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1200&q=85&fit=crop',
            'Librería Catalonia': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1200&q=85&fit=crop',
            'Patio Bellavista': 'https://images.unsplash.com/photo-1555400082-89f07be8007c?w=1200&q=85&fit=crop',
            'Galería Artespacio': 'https://images.unsplash.com/photo-1561214115-f2f134cc4912?w=1200&q=85&fit=crop',
            'Bar The Clinic': 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=1200&q=85&fit=crop',
        }
        
        updated_count = 0
        
        for business_name, new_image_url in image_mapping.items():
            try:
                businesses = Business.objects.filter(name=business_name)
                
                if not businesses.exists():
                    self.stdout.write(
                        self.style.WARNING(f'⚠️  Negocio no encontrado: {business_name}')
                    )
                    continue
                
                for business in businesses:
                    old_image = business.cover_image
                    
                    if dry_run:
                        self.stdout.write(
                            self.style.WARNING(
                                f'[DRY RUN] Actualizaría: {business_name}\n'
                                f'  Imagen actual: {old_image}\n'
                                f'  Nueva imagen: {new_image_url}'
                            )
                        )
                    else:
                        business.cover_image = new_image_url
                        business.save(update_fields=['cover_image'])
                        updated_count += 1
                        
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✅ Actualizado: {business_name}\n'
                                f'   Nueva imagen: {new_image_url}'
                            )
                        )
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error al actualizar {business_name}: {str(e)}')
                )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'\n[DRY RUN] Se actualizarían {len(image_mapping)} negocios'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Actualizados {updated_count} negocios con nuevas imágenes de alta calidad'
                )
            )
