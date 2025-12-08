# 🚀 Quick Start Guide - Ruta Local Backend

Guía rápida para poner en marcha el backend en **5 minutos**.

## ✅ Pre-requisitos

Antes de comenzar, asegúrate de tener instalado:

- [x] Python 3.10+ instalado
- [x] PostgreSQL 15+ instalado y corriendo
- [x] Git

## 📦 Instalación Rápida

### 1. PostgreSQL Setup

Si aún no tienes PostgreSQL, descárgalo: https://www.postgresql.org/download/windows/

**Crear la base de datos:**

```bash
# Opción A: Desde PowerShell
createdb -U postgres rutalocal_dev

# Opción B: Desde pgAdmin o psql
# Abrir psql y ejecutar:
CREATE DATABASE rutalocal_dev;
```

**Configurar password de postgres:**

Si no recuerdas tu password de PostgreSQL, puedes cambiarlo:

```sql
-- En psql como usuario postgres:
ALTER USER postgres WITH PASSWORD 'postgres';
```

### 2. Backend Setup

```bash
# 1. Navegar al directorio del backend
cd C:\Users\Vicente\Documents\GitHub\SantiaGo_backend\backend

# 2. Activar entorno virtual
.\venv\Scripts\Activate

# 3. Instalar dependencias (si no están instaladas)
pip install -r requirements/base.txt

# 4. Verificar configuración de .env
# El archivo .env ya existe, solo verifica que las credenciales sean correctas:
# DB_NAME=rutalocal_dev
# DB_USER=postgres
# DB_PASSWORD=postgres  <-- Cambiar si tu password es diferente
# DB_HOST=localhost
# DB_PORT=5432

# 5. Ejecutar migraciones
python manage.py migrate

# 6. Cargar datos de ejemplo
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/features.json
python manage.py seed_businesses

# 7. Crear superusuario (admin)
python manage.py createsuperuser
# Email: admin@rutalocal.com
# Username: admin
# Password: (tu password)

# 8. Iniciar servidor
python manage.py runserver
```

## 🎉 ¡Listo!

El servidor está corriendo en: **http://localhost:8000**

### Endpoints para probar:

- **API Root:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin
- **Categorías:** http://localhost:8000/api/businesses/categories/
- **Negocios:** http://localhost:8000/api/businesses/

## 🧪 Testing de Endpoints

### 1. Registro de Usuario

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPass123!",
    "password_confirmation": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "user": { ... },
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

### 3. Listar Negocios

```bash
curl http://localhost:8000/api/businesses/
```

### 4. Buscar Negocios por Categoría

```bash
curl http://localhost:8000/api/businesses/?category=cafe
```

## 🔧 Comandos Útiles

### Desarrollo

```bash
# Ver logs detallados
python manage.py runserver --verbosity 3

# Crear nuevas migraciones
python manage.py makemigrations

# Shell interactivo de Django
python manage.py shell

# Recargar fixtures
python manage.py flush  # CUIDADO: Borra todos los datos
python manage.py loaddata fixtures/categories.json fixtures/features.json
```

### Admin

```bash
# Crear más negocios de ejemplo
python manage.py seed_businesses

# Ver todas las URLs disponibles
python manage.py show_urls  # Requiere django-extensions
```

## 🐛 Problemas Comunes

### "No module named 'psycopg'"

```bash
pip install "psycopg[binary]>=3.2.0"
```

### "fe_sendauth: no password supplied"

Verifica las credenciales en `.env`:
```
DB_USER=postgres
DB_PASSWORD=tu_password_aqui
```

### "database 'rutalocal_dev' does not exist"

```bash
createdb -U postgres rutalocal_dev
```

### "Port 8000 is already in use"

```bash
# Windows - matar proceso en puerto 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Luego reiniciar servidor
python manage.py runserver
```

### Error de migraciones

```bash
# Resetear migraciones (CUIDADO: Borra datos)
python manage.py migrate --fake
python manage.py migrate
```

## 📱 Integración con Frontend

El frontend Next.js debe apuntar al backend en desarrollo:

**Frontend `.env.local`:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_PATH=/api
NEXT_PUBLIC_DEV_MODE=false
```

## 🎯 Próximos Pasos

1. **Explorar Admin Panel:** http://localhost:8000/admin
   - Gestionar categorías
   - Crear más negocios
   - Ver reviews y rutas

2. **Probar API con Postman/Thunder Client:**
   - Importar colección de endpoints
   - Probar autenticación JWT
   - Crear rutas personalizadas

3. **Integrar con Frontend:**
   - Iniciar el frontend Next.js
   - Configurar CORS si es necesario
   - Probar registro y login

4. **Agregar Datos Reales:**
   - Agregar negocios de Santiago desde Admin
   - Usar coordenadas reales
   - Agregar imágenes (Cloudinary opcional)

## 📚 Recursos

- **Documentación completa:** `README_BACKEND.md`
- **Requisitos del proyecto:** `../BACKEND_REQUIREMENTS.md`
- **Setup completo:** `../SETUP_COMPLETE.md`
- **Django REST Framework:** https://www.django-rest-framework.org/
- **PostgreSQL Docs:** https://www.postgresql.org/docs/

## 💡 Tips

1. **Usar Django Shell para queries:**
   ```bash
   python manage.py shell
   >>> from apps.businesses.models import Business
   >>> Business.objects.all()
   ```

2. **Ver SQL queries:**
   En `settings/base.py` temporal:
   ```python
   LOGGING = {
       'loggers': {
           'django.db.backends': {
               'level': 'DEBUG',
           }
       }
   }
   ```

3. **Hot reload:**
   El servidor se recarga automáticamente al guardar cambios

4. **Crear fixtures personalizados:**
   ```bash
   python manage.py dumpdata businesses.Category --indent 2 > my_categories.json
   ```

---

## ✅ Checklist de Verificación

Antes de integrar con frontend, verifica:

- [ ] Servidor corriendo en http://localhost:8000
- [ ] Admin panel accesible
- [ ] Al menos 5 negocios en la base de datos
- [ ] Categorías y features cargadas
- [ ] Puedes registrar un usuario
- [ ] Puedes hacer login y recibir token JWT
- [ ] Endpoint /api/businesses/ retorna datos
- [ ] CORS configurado para localhost:3000

## 🚀 ¡Todo Listo!

El backend está completamente funcional y listo para integrarse con el frontend.

**Comando completo de setup (una sola vez):**
```bash
cd backend
.\venv\Scripts\Activate
python manage.py migrate
python manage.py loaddata fixtures/categories.json fixtures/features.json
python manage.py seed_businesses
python manage.py createsuperuser
python manage.py runserver
```

**Comando diario (solo iniciar servidor):**
```bash
cd backend
.\venv\Scripts\Activate
python manage.py runserver
```

---

**¿Necesitas ayuda?** Consulta `README_BACKEND.md` o `SETUP_COMPLETE.md`
