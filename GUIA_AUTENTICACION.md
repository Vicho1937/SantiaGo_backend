# 🔐 GUÍA COMPLETA DE AUTENTICACIÓN - RUTA LOCAL API

Esta guía explica **todas las formas de autenticarte** en la API de Ruta Local.

---

## 📋 TIPOS DE AUTENTICACIÓN DISPONIBLES

Tu API soporta **2 tipos de autenticación**:

### 1. **JWT (JSON Web Tokens)** - Para apps móviles/web
- Usado por el frontend React/Next.js
- No usa sesiones, usa tokens
- Ideal para APIs RESTful

### 2. **Session Auth** - Para la interfaz browsable de DRF
- Usado por la interfaz web de Django Rest Framework
- Usa cookies y sesiones de Django
- Solo para pruebas y desarrollo

---

## 🌐 OPCIÓN 1: INTERFAZ BROWSABLE DE DRF (Navegador Web)

### ¿Qué es?
Es la interfaz web que viene con Django Rest Framework. Se ve así:
- Botones para hacer GET, POST, PUT, DELETE
- Formularios para enviar datos
- Sintaxis resaltada de JSON
- Botón de **"Log in"** en la esquina superior derecha

### ¿Cómo acceder?

**Paso 1: Abre cualquier endpoint en tu navegador**
```
https://web-production-f3cae.up.railway.app/api/
https://web-production-f3cae.up.railway.app/api/businesses/
https://web-production-f3cae.up.railway.app/api/routes/
```

**Paso 2: Busca el botón "Log in"**
- Está en la **esquina superior derecha**
- Dice "Log in" o "Iniciar sesión"

**Paso 3: Click en "Log in"**
Te llevará a:
```
https://web-production-f3cae.up.railway.app/api-auth/login/
```

**Paso 4: Inicia sesión**
- **Usuario**: Tu usuario de Django (email o username)
- **Password**: Tu contraseña

### ⚠️ IMPORTANTE:
- **NO usa JWT**, usa sesiones de Django
- Solo funciona en el navegador
- El usuario debe existir en la base de datos Django
- Puedes crear usuarios desde:
  - Django Admin (`/admin/`)
  - El endpoint de registro (`/api/auth/register/`)
  - Comando `python manage.py createsuperuser`

---

## 🔑 OPCIÓN 2: DJANGO ADMIN (Panel de Administración)

### ¿Cómo acceder?

**URL del Admin**:
```
https://web-production-f3cae.up.railway.app/admin/
```

**Credenciales**:
- Solo usuarios con `is_staff=True` pueden acceder
- Necesitas crear un superusuario primero

### ¿Cómo crear un superusuario?

**Opción A - Desde Railway CLI**:
```bash
railway login
railway link
railway run python backend/manage.py createsuperuser
```

**Opción B - Desde el script en tu repo**:
```bash
# En tu máquina local (conectado a la DB de Railway)
cd ~/Documentos/GitHub/SantiaGo_backend/backend
python create_superuser.py
```

**Opción C - Desde Railway Console**:
1. Ve a Railway Dashboard
2. Abre la terminal del proyecto
3. Ejecuta:
```bash
python backend/manage.py createsuperuser
```

Te pedirá:
- Email
- Username
- Password

### ¿Qué puedes hacer en Django Admin?
- ✅ Ver todos los usuarios
- ✅ Crear/editar/eliminar usuarios
- ✅ Dar permisos de staff/admin
- ✅ Ver rutas, negocios, reviews
- ✅ Configurar permisos granulares

---

## 📱 OPCIÓN 3: JWT PARA APPS/FRONTEND (Programático)

### ¿Cuándo usar JWT?
- Frontend React/Next.js/Vue
- Apps móviles (React Native, Flutter)
- Cualquier cliente que no sea un navegador web

### Flujo de autenticación JWT

#### 1. **REGISTRO (Crear cuenta)**

**Endpoint**: `POST /api/auth/register/`

**Request**:
```bash
curl -X POST https://web-production-f3cae.up.railway.app/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "username": "usuario123",
    "password": "MiPassword123!",
    "password_confirmation": "MiPassword123!",
    "first_name": "Juan",
    "last_name": "Pérez"
  }'
```

**Response**:
```json
{
  "user": {
    "id": "uuid-aqui",
    "email": "usuario@example.com",
    "username": "usuario123",
    "name": "Juan Pérez",
    ...
  },
  "tokens": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "tokenType": "Bearer",
    "expiresIn": 3600  // 60 minutos
  }
}
```

#### 2. **LOGIN (Iniciar sesión)**

**Endpoint**: `POST /api/auth/login/`

**Request**:
```bash
curl -X POST https://web-production-f3cae.up.railway.app/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "MiPassword123!"
  }'
```

**Response**: Mismo formato que registro

#### 3. **USAR EL TOKEN**

Una vez que tengas el `accessToken`, úsalo en todas las peticiones:

**Ejemplo - Ver mi perfil**:
```bash
curl https://web-production-f3cae.up.railway.app/api/auth/me/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Ejemplo - Crear una ruta**:
```bash
curl -X POST https://web-production-f3cae.up.railway.app/api/routes/create/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi Ruta por Santiago",
    "description": "Una ruta increíble",
    "is_public": true,
    "stops": [
      {
        "business_id": "uuid-del-negocio",
        "order": 1,
        "duration": 60,
        "notes": "Primer lugar"
      }
    ]
  }'
```

#### 4. **REFRESH TOKEN (Renovar token expirado)**

Cuando el `accessToken` expire (después de 60 minutos):

**Endpoint**: `POST /api/auth/refresh/`

**Request**:
```bash
curl -X POST https://web-production-f3cae.up.railway.app/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

**Response**:
```json
{
  "access": "nuevo-access-token-aqui",
  "refresh": "nuevo-refresh-token-aqui"  // Si ROTATE_REFRESH_TOKENS está activado
}
```

#### 5. **LOGOUT (Cerrar sesión)**

**Endpoint**: `POST /api/auth/logout/`

**Request**:
```bash
curl -X POST https://web-production-f3cae.up.railway.app/api/auth/logout/ \
  -H "Authorization: Bearer tu-access-token" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "tu-refresh-token"
  }'
```

Esto añade el refresh token a la blacklist para que no se pueda usar más.

---

## 🔒 CONFIGURACIÓN DE PERMISOS ACTUAL

### Configuración global (en `settings.py`):
```python
'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticatedOrReadOnly',
),
```

### ¿Qué significa `IsAuthenticatedOrReadOnly`?

**Endpoints SIN autenticación (público)**:
- ✅ `GET /api/` - Leer lista de endpoints
- ✅ `GET /api/businesses/` - Ver negocios
- ✅ `GET /api/routes/` - Ver rutas públicas (solo las que tienen `is_public=True`)

**Endpoints CON autenticación (protegidos)**:
- 🔒 `POST /api/routes/create/` - Crear ruta
- 🔒 `PATCH /api/routes/<id>/update/` - Actualizar ruta
- 🔒 `DELETE /api/routes/<id>/delete/` - Eliminar ruta
- 🔒 `PATCH /api/users/profile/` - Actualizar perfil

**Endpoints SIEMPRE PÚBLICOS (override con `AllowAny`)**:
- ✅ `POST /api/auth/login/` - Login
- ✅ `POST /api/auth/register/` - Registro

---

## 🛡️ OPCIONES DE SEGURIDAD

### Opción A: Hacer TODA la API privada

En `backend/config/settings/base.py`, cambia:
```python
'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticated',  # ← Cambiar aquí
),
```

**Efecto**:
- ❌ `GET /api/businesses/` requiere autenticación
- ❌ `GET /api/routes/` requiere autenticación
- ✅ `POST /api/auth/login/` sigue siendo público (tiene `@permission_classes([AllowAny])`)

### Opción B: Mantener lectura pública, escritura privada (actual)

```python
'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticatedOrReadOnly',  # ← Actual
),
```

**Efecto**:
- ✅ Cualquiera puede VER negocios y rutas
- 🔒 Solo usuarios autenticados pueden CREAR/EDITAR/ELIMINAR

### Opción C: Permisos granulares por endpoint

Mantener el default y usar decoradores en cada vista:

```python
from rest_framework.permissions import IsAuthenticated, AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])  # ← Público
def business_list(request):
    ...

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # ← Privado
def create_route(request):
    ...
```

---

## 📊 RESUMEN DE RUTAS DE AUTENTICACIÓN

| Ruta | Propósito | Autenticación |
|------|-----------|---------------|
| `/admin/` | Django Admin Panel | Session (staff required) |
| `/api-auth/login/` | Login para DRF Browsable API | Session |
| `/api/auth/login/` | Login JWT para apps/frontend | JWT (genera tokens) |
| `/api/auth/register/` | Registro de usuarios | Público (genera tokens) |
| `/api/auth/me/` | Ver perfil actual | JWT required |
| `/api/auth/refresh/` | Renovar access token | Refresh token required |
| `/api/auth/logout/` | Blacklist del refresh token | JWT required |

---

## 🧪 PRUEBA RÁPIDA

### Test 1: Ver la interfaz browsable de DRF
1. Abre en tu navegador: https://web-production-f3cae.up.railway.app/api/businesses/
2. Deberías ver una interfaz web con JSON formateado
3. En la esquina superior derecha hay un botón "Log in"

### Test 2: Login en la interfaz browsable
1. Click en "Log in"
2. Te lleva a: `/api-auth/login/`
3. Ingresa credenciales de un usuario Django
4. Si no tienes usuario, créalo con `python manage.py createsuperuser`

### Test 3: Probar JWT con curl
```bash
# 1. Hacer login y obtener tokens
curl -X POST https://web-production-f3cae.up.railway.app/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"tu@email.com","password":"tupassword"}'

# 2. Copiar el accessToken de la respuesta

# 3. Usar el token para ver tu perfil
curl https://web-production-f3cae.up.railway.app/api/auth/me/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN_AQUI"
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Error: "Authentication credentials were not provided"
- Olvidaste enviar el header `Authorization: Bearer <token>`
- El token expiró (dura 60 minutos)
- Usa `/api/auth/refresh/` para renovar

### Error: "Invalid token"
- El token está mal copiado
- El token fue blacklisted (hiciste logout)
- La SECRET_KEY del backend cambió

### No puedo hacer login en `/api-auth/login/`
- El usuario no existe en la base de datos
- La contraseña es incorrecta
- Crea un usuario con `createsuperuser`

### El botón "Log in" no aparece en la interfaz browsable
- Asegúrate que `path('api-auth/', include('rest_framework.urls'))` esté en `urls.py`
- Reinicia el servidor

---

## 📝 RECOMENDACIONES

### Para desarrollo:
- Usa `IsAuthenticatedOrReadOnly` (lectura pública, escritura privada)
- Activa la interfaz browsable de DRF
- Crea un superusuario para pruebas

### Para producción:
- Considera cambiar a `IsAuthenticated` (todo privado)
- O deja endpoints de lectura públicos si quieres que la gente explore
- Asegúrate de tener rate limiting
- Usa HTTPS siempre

---

**Última actualización**: 12 de Diciembre 2025
