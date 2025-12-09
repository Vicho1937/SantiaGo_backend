-- Script para corregir errores 500 en Django Admin
-- Agrega los campos faltantes en la tabla businesses y crea la tabla business_owner_profiles

BEGIN;

-- 1. Agregar campos faltantes en la tabla businesses
ALTER TABLE businesses 
ADD COLUMN IF NOT EXISTS created_by_owner BOOLEAN DEFAULT FALSE NOT NULL;

ALTER TABLE businesses 
ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'published' NOT NULL;

ALTER TABLE businesses 
ADD COLUMN IF NOT EXISTS approved_by_id UUID NULL;

ALTER TABLE businesses 
ADD COLUMN IF NOT EXISTS approved_at TIMESTAMP WITH TIME ZONE NULL;

ALTER TABLE businesses 
ADD COLUMN IF NOT EXISTS rejection_reason TEXT DEFAULT '' NOT NULL;

-- 2. Agregar restricción de chequeo para el campo status
ALTER TABLE businesses DROP CONSTRAINT IF EXISTS businesses_status_check;
ALTER TABLE businesses ADD CONSTRAINT businesses_status_check 
CHECK (status IN ('draft', 'pending_review', 'published', 'rejected'));

-- 3. Agregar foreign key para approved_by
ALTER TABLE businesses DROP CONSTRAINT IF EXISTS businesses_approved_by_id_fkey;
ALTER TABLE businesses ADD CONSTRAINT businesses_approved_by_id_fkey 
FOREIGN KEY (approved_by_id) REFERENCES users(id) ON DELETE SET NULL;

-- 4. Crear tabla business_owner_profiles si no existe
CREATE TABLE IF NOT EXISTS business_owner_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE,
    can_create_businesses BOOLEAN DEFAULT FALSE NOT NULL,
    max_businesses_allowed INTEGER DEFAULT 0 NOT NULL,
    is_verified_owner BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT business_owner_profiles_user_id_fkey 
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 5. Crear índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_businesses_status ON businesses(status);
CREATE INDEX IF NOT EXISTS idx_businesses_created_by_owner ON businesses(created_by_owner);
CREATE INDEX IF NOT EXISTS idx_businesses_approved_by ON businesses(approved_by_id);
CREATE INDEX IF NOT EXISTS idx_owner_profiles_user ON business_owner_profiles(user_id);

COMMIT;

-- Verificar que las tablas y columnas existen
SELECT 'Verificación de columnas en businesses:' as mensaje;
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'businesses' 
AND column_name IN ('created_by_owner', 'status', 'approved_by_id', 'approved_at', 'rejection_reason')
ORDER BY column_name;

SELECT 'Verificación de tabla business_owner_profiles:' as mensaje;
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'business_owner_profiles'
ORDER BY ordinal_position;
