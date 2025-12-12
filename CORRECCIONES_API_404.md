# 🔧 CORRECCIONES DE API 404 Y JWT - RAILWAY DEPLOY

**Fecha**: 12 de Diciembre 2025
**Commit**: `530d8bf` - Fix critical API 404 errors and JWT configuration

---

## 🐛 PROBLEMAS SOLUCIONADOS

### 1. **ERROR 404 EN TODOS LOS ENDPOINTS DE API**

**Causa Raíz**: Typo crítico en `/backend/config/urls.py`

```python
# ❌ ANTES (incorrecto)
path('api/auth/', include('apps.auxthentication.urls')),  # Typo: "auxthentication"

# ✅ AHORA (corregido)
path('api/auth/', include('apps.authentication.urls')),  # Correcto: "authentication"
```

Este typo causaba que Django no pudiera importar las URLs de autenticación, resultando en 404 para todos los endpoints.

---

### 2. **ENDPOINT /api/ DABA 404**

**Solución**: Agregado endpoint root que muestra la documentación de la API

```python
# Nuevo endpoint en /api/
def api_root(request):
    """API root endpoint - muestra endpoints disponibles"""
    return JsonResponse({
        'message': 'Ruta Local API',
        'version': '1.0',
        'endpoints': {
            'auth': {
                'login': '/api/auth/login/',
                'register': '/api/auth/register/',
                'logout': '/api/auth/logout/',
                'me': '/api/auth/me/',
                'refresh': '/api/auth/refresh/',
                'google': '/api/auth/google/',
            },
            'users': { ... },
            'businesses': '/api/businesses/',
            'routes': '/api/routes/',
            ...
        }
    })
```

**Ahora puedes visitar**: https://web-production-f3cae.up.railway.app/api/

---

### 3. **JWT EXPIRACIÓN INCORRECTA**

**Problema**: El backend devolvía `expiresIn: 900` (15 min) pero el token real duraba 60 minutos.

**Solución**: Ahora el `expiresIn` se obtiene dinámicamente de la configuración:

```python
def get_tokens_for_user(user):
    """Genera tokens JWT para un usuario"""
    refresh = RefreshToken.for_user(user)

    # Obtener el tiempo de expiración del access token desde settings
    access_token_lifetime = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
    expires_in = int(access_token_lifetime.total_seconds())  # 3600 segundos = 60 min

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'expires_in': expires_in,  # ✅ Ahora retorna 3600
    }
```

---

### 4. **LOGOUT FALLANDO**

**Problema**: La función `token.blacklist()` no funcionaba porque faltaba la app de blacklist.

**Solución**: Agregada `rest_framework_simplejwt.token_blacklist` a `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',  # ✅ Agregado
    ...
]
```

---

### 5. **URL DE REVIEWS CONFUSA**

**Problema**: Reviews estaba en `path('api/', ...)` lo cual era confuso.

**Solución**: Cambiado a `path('api/reviews/', ...)`

---

## ✅ VERIFICACIÓN POST-DEPLOY

### 1. **Verificar que Railway haya detectado el deploy**

Railway debería haber iniciado un nuevo deploy automáticamente. Verifica en:
https://railway.app/dashboard

**Tiempo estimado de deploy**: 3-5 minutos

---

### 2. **Probar el endpoint root de la API**

```bash
curl https://web-production-f3cae.up.railway.app/api/
```

**Respuesta esperada**:
```json
{
  "message": "Ruta Local API",
  "version": "1.0",
  "endpoints": { ... }
}
```

---

### 3. **Probar registro de usuario**

```bash
curl -X POST https://web-production-f3cae.up.railway.app/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPassword123!",
    "password_confirmation": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Respuesta esperada**:
```json
{
  "user": {
    "id": "...",
    "email": "test@example.com",
    ...
  },
  "tokens": {
    "accessToken": "eyJ...",
    "refreshToken": "eyJ...",
    "tokenType": "Bearer",
    "expiresIn": 3600  ✅ Ahora retorna 3600 en lugar de 900
  }
}
```

---

### 4. **Probar login**

```bash
curl -X POST https://web-production-f3cae.up.railway.app/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

---

### 5. **Probar endpoint protegido (me)**

```bash
# Primero obtén el access token del login/registro
ACCESS_TOKEN="eyJ..."

curl https://web-production-f3cae.up.railway.app/api/auth/me/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta esperada**: Información del usuario autenticado

---

### 6. **Probar refresh token**

```bash
REFRESH_TOKEN="eyJ..."

curl -X POST https://web-production-f3cae.up.railway.app/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "'$REFRESH_TOKEN'"
  }'
```

**Respuesta esperada**:
```json
{
  "access": "nuevo_token_aqui",
  "refresh": "nuevo_refresh_token_aqui"
}
```

---

### 7. **Probar logout (blacklist)**

```bash
curl -X POST https://web-production-f3cae.up.railway.app/api/auth/logout/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "'$REFRESH_TOKEN'"
  }'
```

---

## 🚨 ACCIONES ADICIONALES REQUERIDAS

### 1. **Ejecutar migraciones en Railway**

Dado que agregamos `token_blacklist` app, necesitas ejecutar las migraciones:

**Opción A - Desde Railway CLI**:
```bash
railway run python backend/manage.py migrate
```

**Opción B - Desde Railway Dashboard**:
1. Ve a tu proyecto en Railway
2. Settings > Deploy > Custom Start Command
3. Asegúrate que incluya las migraciones:
```bash
python backend/manage.py migrate && python backend/manage.py collectstatic --noinput && gunicorn --chdir backend config.wsgi:application
```

---

### 2. **Verificar variables de entorno en Railway**

Asegúrate que estas variables estén configuradas:

```env
# Django
DEBUG=False
SECRET_KEY=tu-secret-key-segura
ALLOWED_HOSTS=.railway.app,.vercel.app
DJANGO_SETTINGS_MODULE=config.settings  # ✅ IMPORTANTE

# Database
DATABASE_URL=postgresql://...  # Railway provee esto automáticamente

# CORS
CORS_ALLOWED_ORIGINS=https://rutago-nine.vercel.app,https://tu-frontend.vercel.app

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60  # minutos
JWT_REFRESH_TOKEN_LIFETIME=10080  # 7 días

# Otras
FRONTEND_URL=https://tu-frontend.vercel.app
```

---

## 📊 CAMBIOS EN LOS ARCHIVOS

### Archivos modificados:

1. **`backend/config/urls.py`**
   - Corregido typo en import de authentication
   - Agregado endpoint root `/api/`
   - Movido reviews a `/api/reviews/`

2. **`backend/apps/authentication/views.py`**
   - Agregado cálculo dinámico de `expiresIn`
   - Importado `settings` desde Django
   - Modificada función `get_tokens_for_user()`

3. **`backend/config/settings/base.py`**
   - Agregado `rest_framework_simplejwt.token_blacklist` a `INSTALLED_APPS`

---

## 🎯 PRÓXIMOS PASOS

### Ahora que la API funciona:

1. **Conectar el frontend**:
   - El frontend en RUTALOCAL1V ya tiene el `HttpInterceptor` configurado
   - Solo necesita que `NEXT_PUBLIC_API_URL` apunte a Railway

2. **Implementar el guardado de rutas**:
   - El botón "Guardar ruta" en el frontend no está conectado al backend
   - Ver el análisis completo en el reporte anterior

3. **Testing**:
   - Probar todos los endpoints con Postman o Insomnia
   - Verificar que JWT funcione correctamente
   - Probar el flujo completo de login/logout

---

## 📝 NOTAS IMPORTANTES

- El deploy en Railway es automático al hacer push a GitHub
- Revisa los logs en Railway si hay algún error: https://railway.app/dashboard
- La migración de `token_blacklist` se debe ejecutar manualmente
- Los tokens JWT ahora duran **60 minutos** (no 15)
- El refresh token dura **7 días**

---

## 🆘 TROUBLESHOOTING

### Si aún ves 404 en /api/:

1. **Verifica que el deploy haya terminado**:
   - Ve a Railway dashboard
   - Espera a que el deploy muestre "Success"

2. **Verifica los logs**:
   ```bash
   railway logs
   ```

3. **Verifica que las migraciones corrieron**:
   ```bash
   railway run python backend/manage.py showmigrations
   ```

### Si JWT no funciona:

1. **Verifica que `token_blacklist` esté migrado**
2. **Verifica las variables de entorno JWT**
3. **Revisa los logs de Railway para errores**

---

**Estado**: ✅ Cambios aplicados y pusheados a Railway
**Commit**: `530d8bf`
**Branch**: `main`
