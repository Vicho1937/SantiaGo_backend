# 🔗 Coordinación Frontend-Backend

**Fecha:** 8 de Diciembre, 2025  
**Frontend:** https://rutago-nine.vercel.app/  
**Backend:** Por deployar

---

## 🎯 Variables de Entorno Necesarias

### 📱 Frontend (Vercel) - `.env.local` o Variables de Entorno

El frontend necesita estas variables para conectarse al backend:

```bash
# Backend API URL (CRÍTICO)
NEXT_PUBLIC_API_URL=https://tu-proyecto.railway.app
NEXT_PUBLIC_API_BASE_PATH=/api

# Modo desarrollo (false para usar backend real)
NEXT_PUBLIC_DEV_MODE=false

# Mapbox (ya configurado en el frontend)
NEXT_PUBLIC_MAPBOX_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ

# Storage keys (ya configurado)
NEXT_PUBLIC_STORAGE_KEY=santiago_user
NEXT_PUBLIC_TOKEN_KEY=santiago_token

# Google OAuth (opcional)
NEXT_PUBLIC_GOOGLE_CLIENT_ID=tu-client-id
GOOGLE_CLIENT_SECRET=tu-secret
```

---

### 🖥️ Backend (Railway/Render) - Variables de Entorno

El backend necesita estas variables:

```bash
# Django
DEBUG=False
SECRET_KEY=<generar-nueva-key>
ALLOWED_HOSTS=*.railway.app,rutago-nine.vercel.app

# Database (Railway/Render lo provee automáticamente)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# JWT
JWT_SECRET_KEY=<generar-nueva-key>
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080

# CORS (CRÍTICO - debe incluir el dominio del frontend)
CORS_ALLOWED_ORIGINS=https://rutago-nine.vercel.app

# Mapbox (mismo token que frontend)
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ

# Google OAuth (opcional - debe coincidir con frontend)
GOOGLE_CLIENT_ID=<mismo-que-frontend>
GOOGLE_CLIENT_SECRET=<tu-secret>

# Cloudinary (opcional)
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# SendGrid (opcional)
SENDGRID_API_KEY=
DEFAULT_FROM_EMAIL=noreply@rutalocal.com

# Frontend URL
FRONTEND_URL=https://rutago-nine.vercel.app
```

---

## 🔍 Variables que DEBEN Coincidir

### 1. Mapbox Token ✅
**Ya lo tienes en el frontend:**
```
pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ
```

**Usar el MISMO en el backend.**

---

### 2. Google OAuth (si lo usas)

**Frontend necesita:**
```bash
NEXT_PUBLIC_GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
```

**Backend necesita EL MISMO:**
```bash
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com  # ← Mismo valor
GOOGLE_CLIENT_SECRET=xxx  # ← Secret de Google Console
```

**Configuración en Google Console:**
- Authorized JavaScript origins: `https://rutago-nine.vercel.app`
- Authorized redirect URIs: 
  - `https://rutago-nine.vercel.app/auth/google/callback`
  - `https://tu-proyecto.railway.app/api/auth/google/callback`

---

### 3. CORS (CRÍTICO)

**Backend debe permitir el dominio del frontend:**

```python
# En backend/config/settings/production.py
CORS_ALLOWED_ORIGINS = [
    'https://rutago-nine.vercel.app',  # ← Dominio exacto del frontend
]
```

**Si el frontend tiene múltiples dominios:**
```python
CORS_ALLOWED_ORIGINS = [
    'https://rutago-nine.vercel.app',
    'https://www.rutago.com',  # Si tienes dominio custom
]
```

---

## 📋 Checklist de Coordinación

### Antes del Deploy:

- [ ] ¿Tienes el `.env.local` del frontend?
- [ ] ¿Sabes qué variables tiene configuradas?
- [ ] ¿Hay Google OAuth configurado?
- [ ] ¿Hay Cloudinary configurado?
- [ ] ¿El Mapbox token funciona?

### Durante el Deploy:

- [ ] Backend deployado en Railway/Render
- [ ] URL del backend obtenida (ej: `https://santiago-backend-xyz.railway.app`)
- [ ] Variables de entorno configuradas en Railway/Render

### Actualizar Frontend en Vercel:

- [ ] Ir a: https://vercel.com/dashboard
- [ ] Proyecto: rutago-nine
- [ ] Settings → Environment Variables
- [ ] Agregar/Actualizar:
  ```
  NEXT_PUBLIC_API_URL=https://tu-backend.railway.app
  NEXT_PUBLIC_DEV_MODE=false
  ```
- [ ] Guardar cambios
- [ ] Deployments → Redeploy

### Verificación:

- [ ] Abrir: https://rutago-nine.vercel.app
- [ ] Abrir DevTools Console (F12)
- [ ] Verificar NO hay errores de CORS
- [ ] Intentar Login/Register
- [ ] Verificar que carga categorías

---

## 🚨 Errores Comunes

### Error 1: CORS

**Síntoma en Console:**
```
Access to fetch at 'https://backend.com/api/...' from origin 'https://rutago-nine.vercel.app' 
has been blocked by CORS policy
```

**Solución:**
```python
# Backend - settings/production.py
CORS_ALLOWED_ORIGINS = [
    'https://rutago-nine.vercel.app',  # ← Agregar este dominio
]
```

---

### Error 2: API URL incorrecta

**Síntoma en Console:**
```
Failed to fetch
net::ERR_NAME_NOT_RESOLVED
```

**Solución:**
Verificar en Vercel que `NEXT_PUBLIC_API_URL` apunta al backend correcto.

---

### Error 3: Google OAuth falla

**Síntoma:**
```
invalid_client
```

**Solución:**
1. Verificar que `GOOGLE_CLIENT_ID` es el mismo en frontend y backend
2. Verificar que ambos dominios están en Google Console como authorized

---

## 🔐 Generar Claves Secretas

### Para SECRET_KEY (Django):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Ejemplo de output:
```
django-insecure-!x@v3w#8f+5j&9k*2p-7n=1m$4h%6g^0q
```

### Para JWT_SECRET_KEY:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Ejemplo de output:
```
AbCd12EfGh34IjKl56MnOp78QrSt90UvWx12Yz34AbCd56Ef
```

---

## 📝 Plantilla de Variables para Railway

Copia esto y completa:

```bash
# Django
DEBUG=False
SECRET_KEY=<generar con comando arriba>
ALLOWED_HOSTS=*.railway.app,rutago-nine.vercel.app

# Database (Railway lo llena automáticamente)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# JWT
JWT_SECRET_KEY=<generar con comando arriba>
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080

# CORS
CORS_ALLOWED_ORIGINS=https://rutago-nine.vercel.app

# Mapbox
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ

# Frontend
FRONTEND_URL=https://rutago-nine.vercel.app

# Google OAuth (si aplica - dejalo vacío si no lo usas)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Cloudinary (opcional - dejalo vacío por ahora)
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# SendGrid (opcional - dejalo vacío por ahora)
SENDGRID_API_KEY=
DEFAULT_FROM_EMAIL=noreply@rutalocal.com
```

---

## 🤔 ¿Necesitas el .env del Frontend?

### SÍ necesito saber:

1. ✅ **NEXT_PUBLIC_API_BASE_PATH** - ¿Es `/api`?
   - Si es diferente, debo ajustar las URLs del backend

2. ✅ **Google OAuth** - ¿Está configurado?
   - Si sí, necesito el GOOGLE_CLIENT_ID

3. ✅ **Cloudinary** - ¿Lo usa el frontend?
   - Si sí, necesito las credenciales

4. ✅ **Otras APIs** - ¿Usa alguna otra?
   - SendGrid, Sentry, etc.

### NO necesito saber:

- ❌ NEXT_PUBLIC_MAPBOX_TOKEN - Ya lo tienes en el README
- ❌ NEXT_PUBLIC_STORAGE_KEY - Es solo del frontend
- ❌ NEXT_PUBLIC_TOKEN_KEY - Es solo del frontend

---

## 📤 Información que Necesito del Frontend

Por favor comparte (si tienes):

```bash
# 1. ¿Cuál es el API_BASE_PATH actual?
NEXT_PUBLIC_API_BASE_PATH=?

# 2. ¿Hay Google OAuth configurado?
NEXT_PUBLIC_GOOGLE_CLIENT_ID=?
# (Si sí, también necesito el SECRET)

# 3. ¿Hay Cloudinary?
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=?
NEXT_PUBLIC_CLOUDINARY_API_KEY=?

# 4. ¿Otras variables?
# (Si hay más variables NEXT_PUBLIC_* compartelas)
```

---

## 🎯 Resumen

### Información Confirmada:
- ✅ Frontend URL: https://rutago-nine.vercel.app/
- ✅ Mapbox Token: pk.eyJ1IjoibmFjaG8yNTQi...
- ✅ API Base Path: /api (asumido del README)

### Información Pendiente:
- ⚠️  Google OAuth Client ID (¿lo usa?)
- ⚠️  Cloudinary credentials (¿lo usa?)
- ⚠️  Otras APIs del frontend

### Puedo Deploy Sin Esa Info:
✅ **SÍ**, puedo hacer el deploy básico con lo que tengo.

Las APIs opcionales (Google OAuth, Cloudinary) pueden agregarse después.

---

## ✅ Recomendación

### Opción A: Deploy Ahora (sin OAuth ni Cloudinary)

**Pros:**
- Backend funciona en 1 hora
- Login/Register con email funciona
- Negocios y rutas funcionan
- Frontend obtiene datos

**Contras:**
- Sin login con Google (temporal)
- Sin upload de imágenes (temporal)

**Luego agregar:**
- Google OAuth
- Cloudinary
- Otras features

---

### Opción B: Esperamos Variables del Frontend

**Pros:**
- Deploy completo desde el inicio
- Google OAuth funcionando
- Cloudinary funcionando

**Contras:**
- Esperar a tener todas las variables
- Un poco más de setup

---

## 🚀 ¿Qué Hacemos?

**Te recomiendo Opción A:**

1. Deploy backend AHORA sin OAuth/Cloudinary
2. Frontend funciona con login por email
3. Cuando tengas las variables, las agregamos
4. Railway hace redeploy automático

**¿Tienes el .env del frontend a mano para compartir las variables?**

Si no, no hay problema - deploy sin ellas y las agregamos después.

---

**¿Cuál opción prefieres?** 🤔
