"""
Script para actualizar imágenes de negocios directamente via SQL
Ejecutar en Railway Shell o localmente con acceso a la DB
"""

UPDATE_IMAGES_SQL = """
-- Actualizar Café Literario
UPDATE businesses_business 
SET cover_image = 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1200&q=85&fit=crop'
WHERE name = 'Café Literario';

-- Actualizar Librería Catalonia  
UPDATE businesses_business
SET cover_image = 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1200&q=85&fit=crop'
WHERE name = 'Librería Catalonia';

-- Actualizar Patio Bellavista
UPDATE businesses_business
SET cover_image = 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1200&q=85&fit=crop'
WHERE name = 'Patio Bellavista';

-- Actualizar Galería Artespacio
UPDATE businesses_business
SET cover_image = 'https://images.unsplash.com/photo-1578926078395-62e0347a30b5?w=1200&q=85&fit=crop'
WHERE name = 'Galería Artespacio';

-- Actualizar Bar The Clinic
UPDATE businesses_business
SET cover_image = 'https://images.unsplash.com/photo-1572116469696-31de0f17cc34?w=1200&q=85&fit=crop'
WHERE name = 'Bar The Clinic';
"""

if __name__ == '__main__':
    print("SQL para actualizar imágenes:")
    print(UPDATE_IMAGES_SQL)
    print("\nCopia y pega este SQL en Railway Database > Query")
