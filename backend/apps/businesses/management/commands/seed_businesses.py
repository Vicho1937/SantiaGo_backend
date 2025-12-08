from django.core.management.base import BaseCommand
from apps.businesses.models import Business, Category, Feature
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Seed database with sample businesses'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding businesses...')
        
        # Obtener categorías
        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(self.style.ERROR('No categories found. Please load fixtures first.'))
            return
        
        # Obtener features
        features = list(Feature.objects.all())
        
        # Barrios de Santiago
        neighborhoods = [
            'Lastarria', 'Bellavista', 'Providencia', 'Barrio Italia',
            'Yungay', 'Brasil', 'Ñuñoa', 'Las Condes'
        ]
        
        # Comunas
        comunas = [
            'Santiago Centro', 'Providencia', 'Recoleta', 'Ñuñoa',
            'Las Condes', 'Vitacura', 'Independencia'
        ]
        
        # Negocios de ejemplo
        sample_businesses = [
            {
                'name': 'Café Literario',
                'short_description': 'Café acogedor con librería',
                'description': 'Un espacio único que combina café de especialidad con una selección de libros. Perfecto para leer y disfrutar de un buen café.',
                'neighborhood': 'Lastarria',
                'category_slug': 'cafe',
                'lat': -33.437230,
                'lng': -70.638600,
                'price_range': 2
            },
            {
                'name': 'Galería Artespacio',
                'short_description': 'Arte contemporáneo chileno',
                'description': 'Galería dedicada a promover el arte contemporáneo de artistas chilenos emergentes y establecidos.',
                'neighborhood': 'Lastarria',
                'category_slug': 'galeria',
                'lat': -33.437500,
                'lng': -70.639000,
                'price_range': 3
            },
            {
                'name': 'Patio Bellavista',
                'short_description': 'Centro gastronómico y cultural',
                'description': 'Espacio al aire libre con múltiples restaurantes, bares y tiendas de artesanía local.',
                'neighborhood': 'Bellavista',
                'category_slug': 'restaurante',
                'lat': -33.432600,
                'lng': -70.633500,
                'price_range': 2
            },
            {
                'name': 'Librería Catalonia',
                'short_description': 'Librería independiente',
                'description': 'Una de las librerías más emblemáticas de Santiago, con una amplia selección de literatura nacional e internacional.',
                'neighborhood': 'Providencia',
                'category_slug': 'libreria',
                'lat': -33.425800,
                'lng': -70.614500,
                'price_range': 2
            },
            {
                'name': 'Bar The Clinic',
                'short_description': 'Bar temático y bohemio',
                'description': 'Bar icónico de Bellavista con ambiente bohemio, música en vivo y terrazas.',
                'neighborhood': 'Bellavista',
                'category_slug': 'bar-pub',
                'lat': -33.432000,
                'lng': -70.634000,
                'price_range': 2
            },
        ]
        
        created_count = 0
        
        for biz_data in sample_businesses:
            # Buscar categoría
            try:
                category = Category.objects.get(slug=biz_data['category_slug'])
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Category {biz_data['category_slug']} not found"))
                continue
            
            # Verificar si ya existe
            if Business.objects.filter(name=biz_data['name']).exists():
                self.stdout.write(self.style.WARNING(f"Business {biz_data['name']} already exists"))
                continue
            
            # Crear negocio
            business = Business.objects.create(
                name=biz_data['name'],
                short_description=biz_data['short_description'],
                description=biz_data['description'],
                category=category,
                latitude=Decimal(str(biz_data['lat'])),
                longitude=Decimal(str(biz_data['lng'])),
                address=f"{biz_data['neighborhood']}, Santiago",
                neighborhood=biz_data['neighborhood'],
                comuna=random.choice(comunas),
                phone='+56 2 2555 ' + str(random.randint(1000, 9999)),
                email=f"info@{biz_data['name'].lower().replace(' ', '')}.cl",
                website=f"https://www.{biz_data['name'].lower().replace(' ', '')}.cl",
                instagram=f"@{biz_data['name'].lower().replace(' ', '')}",
                price_range=biz_data['price_range'],
                cover_image='https://images.unsplash.com/photo-1554118811-1e0d58224f24',
                rating=Decimal(str(round(random.uniform(4.0, 5.0), 2))),
                review_count=random.randint(10, 200),
                verified=random.choice([True, False]),
                is_active=True,
                hours={
                    'monday': {'open': '09:00', 'close': '22:00'},
                    'tuesday': {'open': '09:00', 'close': '22:00'},
                    'wednesday': {'open': '09:00', 'close': '22:00'},
                    'thursday': {'open': '09:00', 'close': '22:00'},
                    'friday': {'open': '09:00', 'close': '23:00'},
                    'saturday': {'open': '10:00', 'close': '23:00'},
                    'sunday': {'open': '10:00', 'close': '21:00'},
                }
            )
            
            # Agregar features aleatorias
            if features:
                business.features.add(*random.sample(features, min(3, len(features))))
            
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created: {business.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} businesses'))
