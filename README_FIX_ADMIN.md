# 🔧 Solución para Errores 500 en Django Admin

## 📋 Problema Identificado

El panel de administración de Django en producción (Railway) está generando **errores 500** en las siguientes secciones:

- ❌ Favorites
- ❌ Negocios (Businesses)
- ❌ **Perfiles de propietarios (BusinessOwnerProfile)** ⭐ [CRÍTICO]
- ❌ Visits
- ❌ Reviews
- ❌ Paradas de rutas (RouteStops)

### 🐛 Errores Detectados en los Logs de Railway:

```
django.db.utils.ProgrammingError: relation "business_owner_profiles" does not exist
psycopg.errors.UndefinedColumn: column businesses.created_by_owner does not exist
```

**Causa raíz:** La base de datos de producción no tiene las tablas y columnas necesarias que están definidas en los modelos de Django.

---

## ✅ Solución

### Opción 1: Usar el Script Automatizado (RECOMENDADO)

He creado un script que aplica todas las correcciones automáticamente.

#### En Railway:

1. **Accede a la terminal de Railway**
2. **Ejecuta el script:**
   ```bash
   cd backend
   python fix_admin_errors.py
   ```

3. **El script hará:**
   - ✅ Agregar columnas faltantes en `businesses`
   - ✅ Crear tabla `business_owner_profiles`
   - ✅ Aplicar todas las migraciones pendientes
   - ✅ Verificar que todo esté correcto

4. **Reinicia el servicio** en Railway para aplicar los cambios

---

### Opción 2: Aplicar SQL Manualmente

Si el script Python falla, puedes aplicar el SQL directamente.

#### Paso 1: Conectarse a la base de datos de Railway

Desde la terminal de Railway o usando un cliente PostgreSQL:

```bash
psql $DATABASE_URL
```

#### Paso 2: Ejecutar el script SQL

Copia y pega el contenido de `backend/fix_database.sql` o ejecuta:

```bash
psql $DATABASE_URL < backend/fix_database.sql
```

#### Paso 3: Ejecutar migraciones de Django

```bash
cd backend
python manage.py migrate
```

---

### Opción 3: Regenerar Migraciones y Aplicarlas

#### Paso 1: Verificar migraciones pendientes

```bash
cd backend
python manage.py showmigrations
```

#### Paso 2: Aplicar todas las migraciones

```bash
python manage.py migrate businesses
python manage.py migrate reviews
python manage.py migrate routes
python manage.py migrate --run-syncdb
```

---

## 🎯 Cambios Específicos Realizados

### 1. Nueva Migración: `0003_add_owner_fields.py`

Esta migración agrega:

**En el modelo `Business`:**
- `created_by_owner` (Boolean): Indica si el negocio fue creado por su propietario
- `status` (CharField): Estado del negocio (draft, pending_review, published, rejected)
- `approved_by` (ForeignKey): Admin que aprobó el negocio
- `approved_at` (DateTimeField): Fecha de aprobación
- `rejection_reason` (TextField): Razón de rechazo

**Nueva tabla `BusinessOwnerProfile`:**
- `user` (OneToOneField): Usuario propietario
- `can_create_businesses` (Boolean): Permiso para crear negocios
- `max_businesses_allowed` (Integer): Límite de negocios (-1 = ilimitado)
- `is_verified_owner` (Boolean): Propietario verificado

### 2. Script SQL: `fix_database.sql`

Crea todas las estructuras necesarias directamente en PostgreSQL.

### 3. Script Python: `fix_admin_errors.py`

Automatiza todo el proceso de corrección y verificación.

---

## 🚀 Cómo Dar Acceso a Usuarios para Crear Locales

Una vez aplicadas las correcciones, podrás gestionar los permisos de usuarios desde el admin:

### 1. Acceder al Admin de Django

```
https://tu-dominio.railway.app/admin/
```

### 2. Ir a "Perfiles de Propietarios"

```
/admin/businesses/businessownerprofile/
```

### 3. Crear o Editar un Perfil de Usuario

Para dar permiso a un usuario:

1. **Buscar al usuario** o crear un nuevo perfil
2. **Configurar los permisos:**
   - ✅ **Puede crear negocios**: Activar
   - 📊 **Máximo de negocios permitidos**: 
     - `0` = No puede crear ninguno
     - `1`, `2`, `3`... = Límite específico
     - `-1` = Ilimitados
   - ✅ **Propietario verificado**: Activar si es un propietario legítimo

### 4. Acciones Masivas Disponibles

En el listado de perfiles puedes seleccionar varios usuarios y:

- 📝 **Permitir crear 1 negocio**
- 📝 **Permitir crear 3 negocios**
- 📝 **Permitir crear ilimitados**
- 🚫 **Revocar permisos**

---

## 📊 Verificación Post-Aplicación

### 1. Verificar en la base de datos:

```sql
-- Ver columnas de businesses
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'businesses' 
AND column_name IN ('created_by_owner', 'status', 'approved_by_id');

-- Ver tabla de perfiles
SELECT * FROM business_owner_profiles LIMIT 5;
```

### 2. Verificar en el Admin de Django:

Intenta acceder a cada sección que antes daba error:

- ✅ `/admin/businesses/business/`
- ✅ `/admin/businesses/businessownerprofile/` ⭐
- ✅ `/admin/businesses/favorite/`
- ✅ `/admin/businesses/visit/`
- ✅ `/admin/reviews/review/`
- ✅ `/admin/routes/routestop/`

---

## 🔄 Proceso para Deployment en Railway

### Paso 1: Commit y Push

```bash
cd /home/ignvvcio254/Documentos/GitHub/SantiaGo_backend
git add .
git commit -m "fix: Add missing database tables and columns for admin panel"
git push origin main
```

### Paso 2: Railway Auto-Deploy

Railway detectará los cambios y hará redeploy automáticamente.

### Paso 3: Aplicar Migraciones

Una vez deployado, ejecuta en la terminal de Railway:

```bash
python backend/fix_admin_errors.py
```

O manualmente:

```bash
cd backend
python manage.py migrate
```

---

## 🎓 Cómo Funciona el Sistema de Propietarios

### Flujo de Creación de Negocio por Propietario:

1. **Usuario se registra** en el frontend
2. **Admin le da permisos** en `/admin/businesses/businessownerprofile/`
3. **Usuario crea su negocio** desde el frontend
4. **Negocio queda con status** `pending_review`
5. **Admin revisa y aprueba** en `/admin/businesses/business/`
6. **Negocio se publica** con status `published`

### Estados de un Negocio:

- `draft`: Borrador (no visible)
- `pending_review`: Pendiente de revisión por admin
- `published`: Publicado y visible
- `rejected`: Rechazado con razón

---

## 🆘 Troubleshooting

### Si el script falla:

```bash
# Ver logs completos
python backend/fix_admin_errors.py 2>&1 | tee fix_log.txt

# Verificar conexión a BD
python backend/manage.py dbshell
```

### Si persisten errores 500:

```bash
# Ver logs en Railway
railway logs

# Verificar variables de entorno
railway variables

# Forzar sincronización de DB
python manage.py migrate --run-syncdb
```

### Si hay conflictos de migraciones:

```bash
# Ver estado de migraciones
python manage.py showmigrations

# Crear migraciones faltantes
python manage.py makemigrations

# Aplicar específicas
python manage.py migrate businesses 0003_add_owner_fields
```

---

## 📝 Archivos Creados/Modificados

```
backend/
├── apps/
│   └── businesses/
│       └── migrations/
│           └── 0003_add_owner_fields.py     ← Nueva migración
├── fix_database.sql                          ← Script SQL
└── fix_admin_errors.py                       ← Script de corrección

README_FIX_ADMIN.md                          ← Este documento
```

---

## ✨ Resultado Final

Después de aplicar estas correcciones:

✅ Todas las secciones del admin funcionarán sin errores 500
✅ Podrás gestionar permisos de usuarios para crear negocios
✅ Los propietarios podrán crear sus locales desde el frontend
✅ Tendrás control completo sobre aprobaciones y rechazos

---

## 🎯 Próximos Pasos

1. ✅ Aplicar las correcciones usando el script
2. ✅ Verificar que todas las secciones funcionen
3. ✅ Crear perfiles de propietario para usuarios específicos
4. ✅ Probar el flujo completo desde el frontend
5. ✅ Monitorear logs de Railway para confirmar que no hay más errores

---

**¿Necesitas ayuda?** Revisa los logs de Railway o ejecuta el script con verbose:

```bash
python backend/fix_admin_errors.py --verbose
```
