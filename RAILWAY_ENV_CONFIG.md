# 🔧 Configuración de Variables de Entorno para Railway

Este documento contiene todas las variables de entorno que debes configurar en Railway para tu backend Django.

---

## 📋 Variables de Entorno para Railway

Copia y pega estas variables en Railway (Settings → Variables):

### 🔐 Django Settings

```bash
DEBUG=False
SECRET_KEY=super-secret-jwt-key-change-in-production
ALLOWED_HOSTS=*
```

**⚠️ IMPORTANTE:** Cambia `SECRET_KEY` por una clave más segura antes de desplegar en producción.

Para generar una nueva SECRET_KEY segura:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### 🗄️ Database (PostgreSQL - Supabase)

Ya tienes una base de datos en Supabase, así que usa estos valores:

```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres.hdshccvnvizoaumqpepq
DB_PASSWORD=Vicho1937.
DB_HOST=aws-0-us-west-2.pooler.supabase.com
DB_PORT=6543
```

**Nota:** No necesitas crear una base de datos PostgreSQL en Railway, ya que estás usando Supabase.

---

### 🔴 Redis (Cache y Celery)

Si planeas usar Redis para caché y Celery, puedes agregar Redis en Railway:

**Opción 1: Agregar Redis en Railway**
1. En Railway, click en "+ New"
2. Selecciona "Database" → "Redis"
3. Railway creará automáticamente la variable `REDIS_URL`

**Opción 2: Usar Redis externo (como Upstash)**
```bash
REDIS_URL=redis://tu-url-de-redis:6379/0
CELERY_BROKER_URL=redis://tu-url-de-redis:6379/0
```

**Opción 3: Deshabilitar temporalmente Redis**
Si no usas Redis por ahora, puedes omitir estas variables (configura tu Django para no requerirlas).

---

### 🔑 JWT

```bash
JWT_SECRET_KEY=super-secret-jwt-key-change-in-production
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080
```

**⚠️ IMPORTANTE:** Cambia `JWT_SECRET_KEY` por una clave diferente a tu SECRET_KEY de Django.

---

### 🌐 CORS

```bash
CORS_ALLOWED_ORIGINS=https://rutago-nine.vercel.app,http://localhost:3000,http://127.0.0.1:3000
```

**Nota:** Incluye localhost para pruebas locales. Puedes quitarlo cuando estés en producción completa.

---

### 🔐 Google OAuth

```bash
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
GOOGLE_REDIRECT_URI=https://rutago-nine.vercel.app/auth/google/callback
```

**Para configurar:**
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto o selecciona uno existente
3. Ve a "APIs & Services" → "Credentials"
4. Crea "OAuth 2.0 Client ID"
5. En "Authorized JavaScript origins" agrega:
   - `https://rutago-nine.vercel.app`
   - `https://tu-backend.up.railway.app`
6. En "Authorized redirect URIs" agrega:
   - `https://rutago-nine.vercel.app/auth/google/callback`
7. Copia el Client ID y Client Secret y pégalos en las variables

---

### 🗺️ Mapbox

Ya tienes tu token de Mapbox:

```bash
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ
```

---

### 📁 Cloudinary (Opcional)

Si usas Cloudinary para almacenar imágenes:

```bash
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

**Para configurar:**
1. Ve a [Cloudinary](https://cloudinary.com/)
2. Crea una cuenta gratuita
3. En el Dashboard, copia tus credenciales
4. Pégalas en las variables de Railway

---

### 📧 SendGrid (Opcional)

Si usas SendGrid para enviar emails:

```bash
SENDGRID_API_KEY=SG.xxx
DEFAULT_FROM_EMAIL=noreply@rutalocal.com
```

**Para configurar:**
1. Ve a [SendGrid](https://sendgrid.com/)
2. Crea una cuenta
3. Ve a "Settings" → "API Keys"
4. Crea una nueva API Key
5. Pégala en las variables de Railway

---

### 🐛 Sentry (Opcional)

Si usas Sentry para monitoreo de errores:

```bash
SENTRY_DSN=https://xxx@sentry.io/xxx
```

**Para configurar:**
1. Ve a [Sentry.io](https://sentry.io/)
2. Crea un proyecto Django
3. Copia el DSN
4. Pégalo en las variables de Railway

---

### 🌍 Frontend URL

```bash
FRONTEND_URL=https://rutago-nine.vercel.app
```

---

## 📝 Resumen: Variables Mínimas Requeridas

Para que tu aplicación funcione en Railway, necesitas al menos estas variables:

```bash
# Django
DEBUG=False
SECRET_KEY=super-secret-jwt-key-change-in-production
ALLOWED_HOSTS=*

# Database (Supabase)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres.hdshccvnvizoaumqpepq
DB_PASSWORD=Vicho1937.
DB_HOST=aws-0-us-west-2.pooler.supabase.com
DB_PORT=6543

# JWT
JWT_SECRET_KEY=super-secret-jwt-key-change-in-production
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080

# CORS
CORS_ALLOWED_ORIGINS=https://rutago-nine.vercel.app

# Mapbox
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ

# Frontend
FRONTEND_URL=https://rutago-nine.vercel.app
```

---

## 🚀 Cómo agregar las variables en Railway

### Método 1: Una por una

1. Ve a tu proyecto en Railway
2. Selecciona tu servicio Django
3. Ve a la pestaña "Variables"
4. Click en "New Variable"
5. Pega el nombre y valor de cada variable
6. Click en "Add"

### Método 2: Bulk Add (Todas a la vez)

1. Ve a tu proyecto en Railway
2. Selecciona tu servicio Django
3. Ve a la pestaña "Variables"
4. Click en "Raw Editor"
5. Copia y pega TODAS las variables en formato:
   ```
   VARIABLE_NAME=valor
   OTRA_VARIABLE=otro_valor
   ```
6. Click en "Update Variables"

---

## ⚠️ Notas de Seguridad

1. **SECRET_KEY y JWT_SECRET_KEY:** Deben ser diferentes y muy seguras en producción
2. **DB_PASSWORD:** Ya tienes una contraseña, asegúrate de no compartirla públicamente
3. **API Keys:** Nunca subas estas variables a Git (usa .env.example sin valores reales)
4. **DEBUG:** Siempre debe ser `False` en producción

---

## 🔄 Actualizar después del primer deploy

Después de que Railway te dé tu URL de backend (ejemplo: `https://santiago-backend.up.railway.app`), actualiza estas variables en **Vercel**:

```bash
NEXT_PUBLIC_API_URL=https://tu-backend.up.railway.app
```

---

## ✅ Verificación

Después de configurar todas las variables:
1. Railway redesplegará automáticamente
2. Ve a los logs para verificar que no hay errores
3. Prueba tu API visitando: `https://tu-backend.up.railway.app/api/`

---

## 🆘 Troubleshooting

### Error: "Database connection failed"
- Verifica que las credenciales de Supabase sean correctas
- Verifica que Supabase permita conexiones externas (whitelist Railway IPs si es necesario)

### Error: "CORS policy error"
- Verifica que `CORS_ALLOWED_ORIGINS` incluya tu URL de Vercel exacta
- No debe tener espacios: `url1,url2` (correcto) vs `url1, url2` (incorrecto)

### Error: "Invalid JWT"
- Verifica que `JWT_SECRET_KEY` sea la misma en backend (Railway) y frontend (Vercel)

---

## 📚 Referencias

- [Railway Docs](https://docs.railway.app/)
- [Supabase Docs](https://supabase.com/docs)
- [Django Environment Variables](https://django-environ.readthedocs.io/)
