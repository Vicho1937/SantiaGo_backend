# 🚂 Guía de Despliegue en Railway - Backend Django

Esta guía te ayudará a desplegar tu backend Django en Railway y conectarlo con tu frontend en Vercel.

## 📋 Pre-requisitos

- Cuenta en [Railway](https://railway.app/)
- GitHub Desktop o Git instalado
- Código del backend subido a GitHub

---

## 🚀 Paso 1: Preparar el Proyecto

### 1.1 Verificar archivos necesarios

Asegúrate de que tu proyecto tenga estos archivos en la raíz del backend:

```
backend/
├── .env                  # Variables de entorno (NO subir a Git)
├── .env.example         # Ejemplo de variables (SÍ subir a Git)
├── requirements/
│   ├── base.txt
│   └── production.txt
├── manage.py
└── config/
```

### 1.2 Crear archivo `.gitignore`

Si no existe, crea un `.gitignore` en la carpeta `backend/`:

```
# Python
*.pyc
__pycache__/
*.py[cod]
*$py.class

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/staticfiles

# Environment
.env
.venv
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
```

---

## 🎯 Paso 2: Subir a GitHub

1. Abre **GitHub Desktop**
2. Selecciona tu repositorio del backend (`SantiaGo_backend`)
3. Asegúrate de que `.env` **NO** esté en los cambios (debe estar en .gitignore)
4. Haz commit de todos los cambios
5. Push al repositorio remoto

---

## 🚂 Paso 3: Crear Proyecto en Railway

### 3.1 Iniciar sesión en Railway

1. Ve a [railway.app](https://railway.app/)
2. Inicia sesión con GitHub
3. Click en **"New Project"**

### 3.2 Conectar repositorio

1. Selecciona **"Deploy from GitHub repo"**
2. Busca tu repositorio `SantiaGo_backend`
3. Selecciónalo y haz click en **"Deploy Now"**

### 3.3 Configurar Root Directory

Si tu código Django está en una subcarpeta (ejemplo: `backend/`):

1. En Railway, ve a **Settings** → **Build**
2. En **Root Directory**, escribe: `backend`
3. Click en **"Save Changes"**

---

## 🗄️ Paso 4: Configurar PostgreSQL

### 4.1 Agregar PostgreSQL

1. En tu proyecto de Railway, click en **"+ New"**
2. Selecciona **"Database"**
3. Elige **"Add PostgreSQL"**
4. Railway creará automáticamente la base de datos

### 4.2 Variables de entorno automáticas

Railway creará automáticamente estas variables:
- `DATABASE_URL`
- `PGHOST`
- `PGPORT`
- `PGUSER`
- `PGPASSWORD`
- `PGDATABASE`

---

## 🔧 Paso 5: Configurar Variables de Entorno

### 5.1 Acceder a Variables

1. En Railway, selecciona tu servicio Django (no la base de datos)
2. Ve a la pestaña **"Variables"**
3. Click en **"New Variable"**

### 5.2 Variables requeridas

Agrega las siguientes variables de entorno:

#### **Obligatorias:**

```bash
# Django Settings
DEBUG=False
SECRET_KEY=genera-una-clave-secreta-super-segura-aqui
ALLOWED_HOSTS=*

# CORS - Agrega tu dominio de Vercel
CORS_ALLOWED_ORIGINS=https://rutalocal1v.vercel.app,https://tu-dominio-personalizado.com

# Frontend URL
FRONTEND_URL=https://rutalocal1v.vercel.app

# JWT
JWT_SECRET_KEY=otra-clave-secreta-para-jwt
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080
```

#### **Opcionales (según tu proyecto):**

```bash
# Mapbox
MAPBOX_ACCESS_TOKEN=tu-token-de-mapbox

# Google OAuth
GOOGLE_CLIENT_ID=tu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-secret
GOOGLE_REDIRECT_URI=https://rutalocal1v.vercel.app/auth/google/callback

# Cloudinary
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret

# SendGrid
SENDGRID_API_KEY=SG.tu-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@tudominio.com

# Sentry (Error Tracking)
SENTRY_DSN=https://tu-sentry-dsn
```

### 5.3 Generar SECRET_KEY segura

Para generar una SECRET_KEY segura, ejecuta en tu terminal local:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📦 Paso 6: Configurar Build

### 6.1 Crear Procfile

Si no existe, crea un archivo `Procfile` en la carpeta `backend/`:

```
web: gunicorn config.wsgi --bind 0.0.0.0:$PORT
```

### 6.2 Agregar gunicorn a requirements

Asegúrate de que `requirements/production.txt` contenga:

```
-r base.txt
gunicorn
psycopg2-binary
django-environ
```

---

## 🔨 Paso 7: Configurar Deploy Commands

En Railway, ve a **Settings** → **Deploy**:

### Build Command:
```bash
pip install -r requirements/production.txt && python manage.py collectstatic --noinput
```

### Start Command:
```bash
python manage.py migrate && gunicorn config.wsgi --bind 0.0.0.0:$PORT
```

---

## 🌐 Paso 8: Obtener URL del Deployment

1. Una vez desplegado, Railway te dará una URL como:
   ```
   https://santiago-backend-production.up.railway.app
   ```

2. **IMPORTANTE**: Copia esta URL, la necesitarás para configurar el frontend

---

## 🔄 Paso 9: Actualizar CORS

1. Vuelve a las **Variables** de Railway
2. Actualiza `CORS_ALLOWED_ORIGINS` para incluir tu URL de Vercel:
   ```
   https://rutalocal1v.vercel.app
   ```

---

## ✅ Paso 10: Verificar Deployment

### 10.1 Probar API

Abre tu navegador y visita:
```
https://tu-proyecto.up.railway.app/api/
```

Deberías ver la respuesta de la API de Django.

### 10.2 Ver Logs

Si hay errores:
1. En Railway, ve a la pestaña **"Deployments"**
2. Click en el último deployment
3. Ve a **"View Logs"**

---

## 🔐 Paso 11: Configurar Google OAuth (Opcional)

Si usas Google OAuth:

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Selecciona tu proyecto
3. Ve a **Credentials**
4. Edita tu **OAuth 2.0 Client ID**
5. En **Authorized redirect URIs**, agrega:
   ```
   https://rutalocal1v.vercel.app/auth/google/callback
   ```
6. Guarda los cambios
7. Actualiza las variables en Railway con tu `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET`

---

## 🚨 Troubleshooting

### Error: "Application failed to respond"

**Solución:**
- Verifica que `Procfile` esté en la raíz correcta
- Revisa que el comando de inicio sea correcto
- Verifica los logs en Railway

### Error: "Database connection failed"

**Solución:**
- Verifica que PostgreSQL esté corriendo en Railway
- Verifica que las variables `DATABASE_URL` o `PG*` estén configuradas
- Revisa los logs para ver el error específico

### Error: "CORS policy"

**Solución:**
- Verifica que `CORS_ALLOWED_ORIGINS` incluya tu dominio de Vercel
- Asegúrate de que no haya espacios en la variable
- Formato correcto: `https://dominio1.com,https://dominio2.com`

---

## 📝 Siguiente Paso

Una vez que tu backend esté desplegado en Railway, continúa con:

👉 **[Guía de Despliegue en Vercel (Frontend)](../RUTALOCAL1V/DEPLOYMENT_VERCEL.md)**

---

## 🔗 Enlaces Útiles

- [Railway Docs](https://docs.railway.app/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [PostgreSQL on Railway](https://docs.railway.app/databases/postgresql)

---

## 🎉 ¡Listo!

Tu backend Django ahora está desplegado en Railway. Anota tu URL de Railway para configurar el frontend en Vercel.
