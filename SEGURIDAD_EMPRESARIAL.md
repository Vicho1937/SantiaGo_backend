# 🔒 SEGURIDAD EMPRESARIAL - API PROTEGIDA

**Fecha**: 12 de Diciembre 2025

---

## 🎯 CONFIGURACIÓN IMPLEMENTADA

Tu API ahora tiene **seguridad a nivel empresarial**:

### ✅ TODO requiere autenticación por defecto

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # ⬅️ Seguridad empresarial
    ),
}
```

---

## 🚪 PUNTOS DE ENTRADA PÚBLICOS

Solo estos 3 endpoints son públicos (permiten acceso sin autenticación):

### 1. **`/api/token/`** - Punto de entrada principal ⭐

**Propósito**: Obtener tokens JWT usando username/password

**Métodos**:
- ❌ `GET` → Muestra formulario de login de DRF (interfaz browsable)
- ✅ `POST` → Obtiene tokens JWT (programático)

**Uso en navegador**:
```
https://web-production-f3cae.up.railway.app/api/token/
```
Verás un formulario con:
- Username
- Password
- Botón "POST"

**Uso programático (curl)**:
```bash
curl -X POST https://web-production-f3cae.up.railway.app/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "AdminRutaGo",
    "password": "tu_password"
  }'
```

**Respuesta**:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 2. **`/api/auth/login/`** - Login del frontend

**Propósito**: Login para el frontend (formato customizado)

```bash
curl -X POST https://web-production-f3cae.up.railway.app/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "rutagonotificaciones@gmail.com",
    "password": "tu_password"
  }'
```

**Respuesta** (formato custom para el frontend):
```json
{
  "user": { ... },
  "tokens": {
    "accessToken": "...",
    "refreshToken": "...",
    "tokenType": "Bearer",
    "expiresIn": 3600
  }
}
```

---

### 3. **`/api/auth/register/`** - Registro de usuarios

**Propósito**: Crear nuevas cuentas

```bash
curl -X POST https://web-production-f3cae.up.railway.app/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nuevo@email.com",
    "username": "nuevo_usuario",
    "password": "Password123!",
    "password_confirmation": "Password123!",
    "first_name": "Nombre",
    "last_name": "Apellido"
  }'
```

---

## 🔐 ENDPOINTS PROTEGIDOS

**TODOS los demás endpoints requieren autenticación**:

| Endpoint | Requiere Auth | Error sin auth |
|----------|---------------|----------------|
| `/api/` | ✅ | 401 Unauthorized |
| `/api/businesses/` | ✅ | 401 Unauthorized |
| `/api/routes/` | ✅ | 401 Unauthorized |
| `/api/auth/me/` | ✅ | 401 Unauthorized |
| `/api/users/profile/` | ✅ | 401 Unauthorized |

---

## 🌐 FLUJO DE AUTENTICACIÓN EN NAVEGADOR

### Paso 1: Ve a `/api/token/`

```
https://web-production-f3cae.up.railway.app/api/token/
```

Verás la interfaz de DRF con un formulario:
```
Token Obtain Pair
Takes a set of user credentials and returns an access and refresh JSON web
token pair to prove the authentication of those credentials.

Username: [_____________]
Password: [_____________]
          [POST]
```

### Paso 2: Ingresa credenciales

- **Username**: `AdminRutaGo` o `rutagonotificaciones@gmail.com`
- **Password**: Tu contraseña

### Paso 3: Click en "POST"

Te devolverá los tokens:
```json
{
  "access": "eyJ...",
  "refresh": "eyJ..."
}
```

### Paso 4: Ahora puedes ver otros endpoints

Una vez autenticado en la sesión, puedes navegar a:
- `/api/businesses/` ✅
- `/api/routes/` ✅
- `/api/` ✅

**Sin autenticarte primero en `/api/token/`**, todos darán error 401.

---

## 🔑 FLUJO DE AUTENTICACIÓN PROGRAMÁTICO (JWT)

### Opción A: Usar `/api/token/` (Standard JWT)

```bash
# 1. Obtener tokens
curl -X POST https://web-production-f3cae.up.railway.app/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"AdminRutaGo","password":"tu_password"}'

# 2. Usar el access token
curl https://web-production-f3cae.up.railway.app/api/businesses/ \
  -H "Authorization: Bearer eyJ..."
```

### Opción B: Usar `/api/auth/login/` (Custom para frontend)

```bash
# 1. Login
curl -X POST https://web-production-f3cae.up.railway.app/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"rutagonotificaciones@gmail.com","password":"tu_password"}'

# 2. Usar el accessToken
curl https://web-production-f3cae.up.railway.app/api/businesses/ \
  -H "Authorization: Bearer eyJ..."
```

---

## 🛡️ NIVELES DE SEGURIDAD

### Nivel 1: Sin autenticación ❌

```bash
curl https://web-production-f3cae.up.railway.app/api/businesses/
```

**Respuesta**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Nivel 2: Con JWT Token ✅

```bash
curl https://web-production-f3cae.up.railway.app/api/businesses/ \
  -H "Authorization: Bearer eyJ..."
```

**Respuesta**:
```json
{
  "success": true,
  "data": [ ... negocios ... ]
}
```

### Nivel 3: Con Session (Navegador) ✅

1. Autentica en `/api/token/` vía formulario
2. La sesión se guarda en cookies
3. Puedes navegar libremente por la API en el navegador

---

## 📊 COMPARACIÓN CON PROYECTO DE REFERENCIA

Tu proyecto ahora funciona **EXACTAMENTE** como `vistcontrol`:

### vistcontrol.up.railway.app:
```
/api/token/ → Muestra formulario ✅
Sin auth en /api/visitas/ → 401 ✅
Con auth en /api/visitas/ → Muestra datos ✅
```

### web-production-f3cae.up.railway.app:
```
/api/token/ → Muestra formulario ✅
Sin auth en /api/businesses/ → 401 ✅
Con auth en /api/businesses/ → Muestra datos ✅
```

---

## 🔄 REFRESH TOKEN

Cuando el access token expire (60 minutos):

```bash
curl -X POST https://web-production-f3cae.up.railway.app/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"tu_refresh_token"}'
```

**Respuesta**:
```json
{
  "access": "nuevo_access_token"
}
```

---

## 🚨 EXCEPCIONES DE SEGURIDAD

Solo estos 3 endpoints ignoran la regla global de autenticación:

1. **`/api/token/`** - Tiene `permission_classes` configurado por SimpleJWT
2. **`/api/auth/login/`** - Tiene `@permission_classes([AllowAny])`
3. **`/api/auth/register/`** - Tiene `@permission_classes([AllowAny])`

Todos los demás heredan `IsAuthenticated` del `DEFAULT_PERMISSION_CLASSES`.

---

## 🧪 PRUEBA RÁPIDA

### Test 1: Verificar que esté protegido

```bash
curl https://web-production-f3cae.up.railway.app/api/businesses/
```

**Esperado**: `{"detail":"Authentication credentials were not provided."}`

### Test 2: Obtener token

```bash
curl -X POST https://web-production-f3cae.up.railway.app/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"AdminRutaGo","password":"tu_password"}'
```

**Esperado**: `{"access":"...","refresh":"..."}`

### Test 3: Acceder con token

```bash
curl https://web-production-f3cae.up.railway.app/api/businesses/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

**Esperado**: Lista de negocios

---

## ✅ BENEFICIOS DE ESTA CONFIGURACIÓN

### Seguridad:
- ✅ No se expone información sin autenticación
- ✅ Protección contra scraping
- ✅ Control total de quién accede a qué
- ✅ Trazabilidad de usuarios

### Flexibilidad:
- ✅ Frontend puede usar `/api/auth/login/` (formato custom)
- ✅ Otros clientes pueden usar `/api/token/` (standard JWT)
- ✅ Navegador puede usar la interfaz browsable de DRF
- ✅ Django Admin sigue funcionando independientemente

### Estándares:
- ✅ Sigue las mejores prácticas de DRF
- ✅ Compatible con SimpleJWT estándar
- ✅ Compatible con cualquier cliente REST

---

## 🔐 CREDENCIALES DEL SUPERUSUARIO

**Username**: `AdminRutaGo`
**Email**: `rutagonotificaciones@gmail.com`
**Password**: *(Verifica en tus registros)*

Si no recuerdas la contraseña, usa el script:
```bash
railway run python backend/reset_admin_password.py
```

---

## 📝 RESUMEN

**Antes** (IsAuthenticatedOrReadOnly):
- ✅ GET /api/businesses/ → Público
- 🔒 POST /api/businesses/ → Privado

**Ahora** (IsAuthenticated):
- 🔒 GET /api/businesses/ → Privado
- 🔒 POST /api/businesses/ → Privado
- ✅ POST /api/token/ → Público (solo para login)
- ✅ POST /api/auth/login/ → Público (solo para login)
- ✅ POST /api/auth/register/ → Público (solo para registro)

---

**🎯 Seguridad empresarial implementada correctamente** ✅
