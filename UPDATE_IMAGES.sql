-- SQL para actualizar imágenes de negocios en Railway
-- Ejecutar en: Railway Dashboard > Database > Query

-- 1. Café Literario (Café con libros en el fondo)
UPDATE businesses_business 
SET cover_image = 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1200&q=85&fit=crop'
WHERE name = 'Café Literario';

-- 2. Librería Catalonia (Estanterías llenas de libros)
UPDATE businesses_business
SET cover_image = 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1200&q=85&fit=crop'
WHERE name = 'Librería Catalonia';

-- 3. Patio Bellavista (Restaurante con terraza)
UPDATE businesses_business
SET cover_image = 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1200&q=85&fit=crop'
WHERE name = 'Patio Bellavista';

-- 4. Galería Artespacio (Galería de arte contemporáneo)
UPDATE businesses_business
SET cover_image = 'https://images.unsplash.com/photo-1578926078395-62e0347a30b5?w=1200&q=85&fit=crop'
WHERE name = 'Galería Artespacio';

-- 5. Bar The Clinic (Bar moderno con luces)
UPDATE businesses_business
SET cover_image = 'https://images.unsplash.com/photo-1572116469696-31de0f17cc34?w=1200&q=85&fit=crop'
WHERE name = 'Bar The Clinic';

-- Verificar las actualizaciones
SELECT name, cover_image FROM businesses_business 
WHERE name IN ('Café Literario', 'Librería Catalonia', 'Patio Bellavista', 'Galería Artespacio', 'Bar The Clinic');
