# 🚂 Configuración Rápida de Railway

## Paso 1: Hacer Commit y Push

Los archivos de configuración ya están listos. Ahora necesitas subirlos a GitHub:

1. Abre **GitHub Desktop**
2. Verifica que estos archivos aparezcan en los cambios:
   - `nixpacks.toml` (raíz del proyecto)
   - `backend/nixpacks.toml`
   - `backend/Procfile`
   - `backend/runtime.txt`
   - `backend/.env` (actualizado)

3. Haz commit con el mensaje: `Configure Railway deployment with Nixpacks`
4. Push a GitHub

---

## Paso 2: Variables de Entorno en Railway

Ve a Railway → Tu proyecto → Variables → Raw Editor y pega esto:

```
DEBUG=False
SECRET_KEY=super-secret-jwt-key-change-in-production
ALLOWED_HOSTS=*
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres.hdshccvnvizoaumqpepq
DB_PASSWORD=Vicho1937.
DB_HOST=aws-0-us-west-2.pooler.supabase.com
DB_PORT=6543
JWT_SECRET_KEY=super-secret-jwt-key-change-in-production
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080
CORS_ALLOWED_ORIGINS=https://rutago-nine.vercel.app,http://localhost:3000
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ
FRONTEND_URL=https://rutago-nine.vercel.app
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
GOOGLE_REDIRECT_URI=https://rutago-nine.vercel.app/auth/google/callback
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
SENDGRID_API_KEY=SG.xxx
DEFAULT_FROM_EMAIL=noreply@rutalocal.com
SENTRY_DSN=https://xxx@sentry.io/xxx
```

**Importante:** Si no usas Google OAuth, Cloudinary, SendGrid o Sentry, puedes omitir esas variables.

---

## Paso 3: Configurar Root Directory en Railway

1. En Railway, ve a **Settings**
2. Busca la sección **Build**
3. En **Root Directory** deja vacío o pon: `.` (punto)
4. **NO** pongas `backend` - el nixpacks.toml ya maneja eso

---

## Paso 4: Redeploy

1. Railway detectará los cambios automáticamente
2. O puedes forzar un redeploy desde la UI de Railway
3. Verifica los logs para asegurarte de que no haya errores

---

## ¿Qué hace cada archivo?

### `nixpacks.toml` (raíz)
Le dice a Railway:
- Instalar Python 3.10
- Ejecutar `pip install` en la carpeta backend
- Ejecutar `collectstatic` para archivos estáticos
- Iniciar con gunicorn

### `backend/Procfile`
Define comandos de:
- **release:** Migraciones y datos iniciales
- **web:** Servidor gunicorn

### `backend/runtime.txt`
Especifica la versión de Python: 3.10.14

---

## Troubleshooting

### Error: "pip: command not found"
**Solución:** Asegúrate de que `nixpacks.toml` esté en la raíz del proyecto (no en `backend/`)

### Error: "No module named 'django'"
**Solución:** Verifica que `requirements/production.txt` incluya todas las dependencias necesarias

### Error: "Database connection failed"
**Solución:** Verifica que las variables de entorno de Supabase estén correctas en Railway

### Error: "collectstatic failed"
**Solución:** Puede ser normal en el primer deploy. Si persiste, temporalmente puedes comentar el comando collectstatic en `nixpacks.toml`

---

## Verificación Final

Una vez desplegado exitosamente:

1. Railway te dará una URL como: `https://web-production-xxxx.up.railway.app`
2. Visita: `https://tu-url.up.railway.app/api/`
3. Deberías ver la respuesta de tu API Django

---

## Siguiente Paso

Una vez que tengas la URL de Railway, actualiza el frontend en Vercel:

1. Ve a Vercel → Tu proyecto → Settings → Environment Variables
2. Actualiza `NEXT_PUBLIC_API_URL` con tu URL de Railway
3. Redeploy el frontend en Vercel

¡Listo! Tu app estará completamente conectada.
