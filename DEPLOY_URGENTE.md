# 🚨 DEPLOY URGENTE - Frontend en Producción

**FECHA:** 8 de Diciembre, 2025  
**ESTADO:** ⚠️ CRÍTICO - Frontend en producción esperando backend

---

## ⚠️ SITUACIÓN ACTUAL

### Frontend YA está en Producción:
```
🌐 URL: https://rutago-nine.vercel.app/
✅ Estado: ONLINE
⚠️ Backend: Apuntando a API inexistente
```

**Esto significa que el backend debe estar en producción LO ANTES POSIBLE.**

---

## 🔴 PRIORIDAD CRÍTICA

El frontend en producción necesita un backend funcionando **AHORA**. 

### Opciones:

#### Opción 1: Deploy Rápido (RECOMENDADO - 2 horas)
Deploy el backend actual "as is" en Railway/Render y luego mejora.

#### Opción 2: Implementar + Deploy (4-6 horas)
Implementa cambios críticos primero, luego deploy.

---

## 🚀 OPCIÓN 1: Deploy Rápido (RECOMENDADO)

### Paso 1: Deploy en Railway (30 min)

**Railway es la opción más rápida:**

1. **Crear cuenta en Railway:**
   - https://railway.app
   - Login con GitHub

2. **Nuevo Proyecto:**
   - "New Project" → "Deploy from GitHub repo"
   - Seleccionar: `SantiaGo_backend`

3. **Agregar PostgreSQL:**
   - "New" → "Database" → "PostgreSQL"
   - Railway crea DB automáticamente

4. **Variables de Entorno:**
   ```bash
   DEBUG=False
   SECRET_KEY=<generar-nueva-key-segura>
   ALLOWED_HOSTS=*.railway.app,rutago-nine.vercel.app
   
   # Database (Railway las provee automáticamente)
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   
   # JWT
   JWT_SECRET_KEY=<generar-nueva-key-segura>
   JWT_ACCESS_TOKEN_LIFETIME=60
   JWT_REFRESH_TOKEN_LIFETIME=10080
   
   # CORS (CRÍTICO)
   CORS_ALLOWED_ORIGINS=https://rutago-nine.vercel.app,https://rutago-nine.vercel.app/
   
   # Mapbox
   MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ
   
   # Frontend URL
   FRONTEND_URL=https://rutago-nine.vercel.app
   ```

5. **Deploy:**
   - Railway hace deploy automático
   - Esperar ~5 minutos

6. **Migraciones:**
   - En Railway dashboard → Service → Shell
   ```bash
   python manage.py migrate
   python manage.py loaddata fixtures/01_categories.json
   python manage.py loaddata fixtures/02_features.json
   python manage.py createsuperuser
   ```

7. **Obtener URL:**
   - Railway provee URL: `https://tu-proyecto.railway.app`

### Paso 2: Actualizar Frontend Vercel (10 min)

1. **Ir a Vercel Dashboard:**
   - https://vercel.com
   - Proyecto: rutago-nine

2. **Settings → Environment Variables:**
   ```bash
   NEXT_PUBLIC_API_URL=https://tu-proyecto.railway.app
   NEXT_PUBLIC_API_BASE_PATH=/api
   NEXT_PUBLIC_DEV_MODE=false
   ```

3. **Redeploy:**
   - Deployments → Últimos → "Redeploy"

### Paso 3: Verificar (10 min)

1. **Backend Health Check:**
   ```bash
   curl https://tu-proyecto.railway.app/api/categories/
   ```

2. **Frontend:**
   - Abrir: https://rutago-nine.vercel.app
   - Intentar login/register
   - Ver si carga categorías

---

## 🎯 OPCIÓN 2: Implementar + Deploy (Si tienes tiempo)

### Fase 1: Cambios Críticos (3 horas)

**HACER ANTES DE DEPLOY:**

1. **Actualizar Serializers** (1 hora)
   - Formato `location` correcto
   - Campos calculados necesarios
   
2. **Actualizar Views** (1 hora)
   - Usar `success_response()` y `error_response()`
   - Formato de respuesta consistente

3. **Filtros Básicos** (1 hora)
   - Filtro por categoría
   - Búsqueda por distancia básica
   - Paginación

**LUEGO:**
4. Deploy en Railway (siguiendo pasos de Opción 1)

---

## 📝 Configuración de Producción

### Backend Settings (Django)

**Crear: `backend/config/settings/production.py`**

```python
from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    '.railway.app',
    'rutago-nine.vercel.app',
    '.vercel.app',
]

# Security
SECRET_KEY = env('SECRET_KEY')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS
CORS_ALLOWED_ORIGINS = [
    'https://rutago-nine.vercel.app',
]
CORS_ALLOW_CREDENTIALS = True

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL'),
        conn_max_age=600
    )
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Railway Configuration

**Crear: `railway.toml`**

```toml
[build]
builder = "NIXPACKS"
buildCommand = "pip install -r requirements/production.txt && python manage.py collectstatic --noinput"

[deploy]
startCommand = "python manage.py migrate && gunicorn config.wsgi:application"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### Procfile (alternativo)

**Crear: `Procfile`**

```
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate
```

### Requirements (Producción)

**Ya actualizado:** `backend/requirements/production.txt`

Incluye:
- ✅ `gunicorn` - Servidor WSGI
- ✅ `dj-database-url` - Parse DATABASE_URL
- ✅ `psycopg2-binary` - PostgreSQL driver
- ✅ `whitenoise` - Servir archivos estáticos
- ✅ `python-decouple` - Variables de entorno

---

## ⚡ Comandos Rápidos

### Generar SECRET_KEY

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Test CORS

```bash
curl -H "Origin: https://rutago-nine.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://tu-proyecto.railway.app/api/auth/login
```

### Ver Logs (Railway)

```bash
railway logs
```

---

## 🔍 Checklist de Deploy

### Pre-Deploy:
- [ ] `DEBUG=False` en settings de producción
- [ ] `SECRET_KEY` único y seguro
- [ ] `ALLOWED_HOSTS` configurado correctamente
- [ ] CORS permite `rutago-nine.vercel.app`
- [ ] Requirements de producción actualizados
- [ ] Database URL configurada

### Durante Deploy:
- [ ] Railway conectado al repo de GitHub
- [ ] PostgreSQL agregado
- [ ] Variables de entorno configuradas
- [ ] Build exitoso
- [ ] Migraciones ejecutadas
- [ ] Fixtures cargados

### Post-Deploy:
- [ ] Backend responde (health check)
- [ ] CORS funciona (sin errores en console)
- [ ] Frontend puede hacer requests
- [ ] Login/Register funcionan
- [ ] Categorías cargan
- [ ] Crear superusuario para admin

---

## 🐛 Troubleshooting

### Error: CORS

**Síntoma:** Frontend muestra error de CORS en console

**Solución:**
```python
# En settings/production.py
CORS_ALLOWED_ORIGINS = [
    'https://rutago-nine.vercel.app',
]
CORS_ALLOW_ALL_ORIGINS = False  # No usar en producción
```

### Error: 500 Internal Server Error

**Solución:**
1. Ver logs en Railway
2. Verificar `DEBUG=False`
3. Verificar `ALLOWED_HOSTS`
4. Verificar Database URL

### Error: Static Files 404

**Solución:**
```bash
python manage.py collectstatic --noinput
```

Agregar a `settings/production.py`:
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## 📊 Tiempo Estimado

| Opción | Tiempo Total | Riesgo |
|--------|--------------|--------|
| **Opción 1: Deploy Rápido** | **2 horas** | Bajo - Backend funciona pero sin optimizaciones |
| **Opción 2: Implementar + Deploy** | **4-6 horas** | Medio - Más features pero más tiempo |

---

## 💡 Recomendación Final

### ✅ HAZ ESTO AHORA (Opción 1):

1. **Deploy en Railway** (30 min)
   - Backend actual funcionando
   - PostgreSQL incluido
   - HTTPS automático

2. **Conectar con Frontend** (10 min)
   - Variables en Vercel
   - Redeploy

3. **Verificar** (10 min)
   - Login funciona
   - Categorías cargan

**Total: 1 hora para tener algo en producción**

### 🔄 LUEGO MEJORA (Gradual):

4. **Implementar cambios FASE 1** (3-4 horas)
   - Formato de respuestas
   - Filtros avanzados
   - Redeploy en Railway (automático)

5. **Implementar FASE 2** (4-5 horas)
   - Dashboard
   - Likes
   - Review stats

---

## 🚀 Empezar Ahora

```bash
# 1. Crear cuenta Railway
https://railway.app

# 2. Conectar GitHub repo
SantiaGo_backend

# 3. Agregar PostgreSQL
Database → PostgreSQL

# 4. Configurar variables de entorno
(Ver lista arriba)

# 5. Deploy automático
Railway hace el resto

# 6. Ejecutar migraciones
python manage.py migrate
python manage.py loaddata fixtures/01_categories.json
python manage.py loaddata fixtures/02_features.json

# 7. Actualizar Vercel
NEXT_PUBLIC_API_URL=https://tu-proyecto.railway.app
```

---

## ✅ Resultado Esperado

**En 1-2 horas tendrás:**

✅ Backend en producción (Railway)  
✅ Frontend conectado al backend  
✅ HTTPS funcionando  
✅ Database PostgreSQL  
✅ Login/Register funcionando  
✅ Categorías cargadas  
✅ CORS configurado  

**Luego puedes mejorar gradualmente siguiendo IMPLEMENTATION_PLAN.md**

---

## 📞 Links Útiles

- **Railway:** https://railway.app
- **Frontend en Producción:** https://rutago-nine.vercel.app
- **Vercel Dashboard:** https://vercel.com/dashboard
- **Documentación Railway:** https://docs.railway.app

---

**¡DEPLOY AHORA!** ⚡

El frontend está esperando. Con Railway puedes tener el backend funcionando en menos de 1 hora.

---

**Última actualización:** 8 de Diciembre, 2025  
**Prioridad:** 🔴 CRÍTICA - Frontend en producción sin backend
