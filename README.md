# 🗺️ Ruta Local - Backend API

Backend API REST para la plataforma Ruta Local, construida con Django REST Framework.

**Última actualización:** 8 de Diciembre, 2025

---

## 🚨 URGENTE - Deploy Necesario

**Frontend en Producción:** https://rutago-nine.vercel.app/ (✅ ONLINE)  
**Backend:** ⚠️ NO EN PRODUCCIÓN

👉 **Lee primero:** [LEEME_PRIMERO.md](LEEME_PRIMERO.md) → [DEPLOY_URGENTE.md](DEPLOY_URGENTE.md)

**Deploy en Railway/Render: 1-2 horas**

---

## 🚀 Inicio Rápido

### 🏃 Desarrollo Local (10-15 minutos)

**Guía completa:** [QUICK_START.md](QUICK_START.md) 👈 Lee esto para ejecutar localmente

**Resumen ultra rápido:**
```bash
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Instalar dependencias
cd backend
pip install -r requirements/development.txt

# 3. Configurar .env
cp .env.example .env
# Editar .env con tus credenciales

# 4. Base de datos y fixtures
python manage.py migrate
python manage.py loaddata fixtures/01_categories.json
python manage.py loaddata fixtures/02_features.json

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Ejecutar servidor
python manage.py runserver
# http://localhost:8000
```

**O usa el script automático:**
```bash
QUICK_SETUP.bat  # Windows
```

### 🌐 Deploy a Producción (1-2 horas)

**Guía completa:** [DEPLOY_URGENTE.md](DEPLOY_URGENTE.md) 👈 Deploy en Railway/Render

---

## 📚 Documentación

### 📖 Guías de Implementación
- **[README_ACTUALIZACION.md](README_ACTUALIZACION.md)** - 👈 **EMPIEZA AQUÍ** - Guía de actualización
- **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** - Plan detallado de tareas
- **[BACKEND_UPDATE_SUMMARY.md](BACKEND_UPDATE_SUMMARY.md)** - Resumen de cambios

### 📖 Documentación del Frontend
- **[BACKEND_README.md](BACKEND_README.md)** - Especificaciones completas de API (del frontend)
- **[BACKEND_REQUIREMENTS.md](BACKEND_REQUIREMENTS.md)** - Requerimientos detallados

### 📖 Documentación Técnica
- **[backend/README_BACKEND.md](backend/README_BACKEND.md)** - Guía técnica del backend

---

## 🎯 Estado del Proyecto

### ✅ Implementado
- Django 5.0 + Django REST Framework
- Modelos completos (User, Business, Category, Route, Review, etc.)
- Autenticación JWT
- CRUD básico de todas las entidades
- CORS configurado
- Admin panel
- Fixtures de categorías y features

### ⚠️ En Progreso
- Formato de respuestas estandarizado
- Filtros avanzados de negocios
- Dashboard con estadísticas
- Endpoints de likes
- Review stats

### 📋 Por Hacer
- Datos de ejemplo (50+ negocios)
- Google OAuth completo
- Rate limiting
- Tests unitarios
- Deploy en producción

---

## 🛠️ Stack Tecnológico

- **Framework:** Django 5.0 + Django REST Framework 3.14
- **Base de Datos:** PostgreSQL 15+
- **Autenticación:** JWT (djangorestframework-simplejwt)
- **CORS:** django-cors-headers
- **Cache:** Redis (opcional)
- **Storage:** Cloudinary / AWS S3

---

## 📂 Estructura del Proyecto

```
SantiaGo_backend/
├── README.md                      ← Este archivo
├── README_ACTUALIZACION.md        ← 👈 GUÍA DE ACTUALIZACIÓN
├── IMPLEMENTATION_PLAN.md         ← Plan detallado
├── BACKEND_UPDATE_SUMMARY.md      ← Resumen de cambios
├── QUICK_SETUP.bat                ← Setup automático
│
└── backend/
    ├── apps/
    │   ├── authentication/        ← Auth y usuarios
    │   ├── businesses/            ← Negocios locales
    │   ├── routes/                ← Rutas personalizadas
    │   └── reviews/               ← Reviews y ratings
    │
    ├── core/
    │   ├── responses.py           ← ✨ Utilidades de respuesta
    │   └── utils.py               ← ✨ Utilidades comunes
    │
    ├── fixtures/
    │   ├── 01_categories.json     ← ✨ 12 categorías
    │   └── 02_features.json       ← ✨ 10 características
    │
    ├── config/                    ← Configuración Django
    ├── manage.py
    └── .env.example
```

---

## 🔌 API Endpoints

### Base URL
```
Desarrollo: http://localhost:8000/api
Producción: https://api.rutalocal.com/api
```

### Principales Endpoints

**Autenticación:**
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/auth/logout`

**Negocios:**
- `GET /api/businesses/` (con filtros avanzados)
- `GET /api/businesses/:id`
- `POST /api/businesses/:id/favorite`
- `POST /api/businesses/:id/visit`

**Rutas:**
- `GET /api/routes/`
- `POST /api/routes/`
- `GET /api/routes/:id`
- `PUT /api/routes/:id`
- `DELETE /api/routes/:id`

**Reviews:**
- `GET /api/businesses/:id/reviews`
- `POST /api/businesses/:id/reviews`

Ver especificaciones completas en [BACKEND_README.md](BACKEND_README.md)

---

## ⚙️ Variables de Entorno

Copiar `.env.example` a `.env` y configurar:

```bash
# Django
DEBUG=True
SECRET_KEY=tu-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=rutalocal_dev
DB_USER=postgres
DB_PASSWORD=tu-password
DB_HOST=localhost
DB_PORT=5432

# JWT
JWT_SECRET_KEY=tu-jwt-secret
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Mapbox
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ

# Cloudinary (opcional)
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# Google OAuth (opcional)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

---

## 🧪 Testing

### Con Frontend

1. **Backend:** `python manage.py runserver` (puerto 8000)
2. **Frontend:** `npm run dev` (puerto 3000)
3. En frontend, configurar `.env.local`:
   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_DEV_MODE=false
   ```

### Con Postman/Thunder Client

```bash
# Register
POST http://localhost:8000/api/auth/register
{
  "name": "Test User",
  "email": "test@test.com",
  "password": "Test123!",
  "password_confirmation": "Test123!"
}

# Login
POST http://localhost:8000/api/auth/login
{
  "email": "test@test.com",
  "password": "Test123!"
}

# Get businesses
GET http://localhost:8000/api/businesses/
```

---

## 📝 Comandos Útiles

```bash
cd backend

# Activar entorno virtual
venv\Scripts\activate

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Cargar fixtures
python manage.py loaddata fixtures\01_categories.json
python manage.py loaddata fixtures\02_features.json

# Superusuario
python manage.py createsuperuser

# Servidor
python manage.py runserver

# Shell
python manage.py shell

# Tests
python manage.py test
```

---

## 🚀 Deploy

### Railway (Recomendado)
1. Conectar repositorio GitHub
2. Configurar variables de entorno
3. PostgreSQL incluido
4. Deploy automático

### Render
1. Conectar repositorio
2. Configurar build command: `pip install -r requirements/production.txt`
3. Start command: `gunicorn config.wsgi:application`

Ver guía completa en [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)

---

## 🤝 Integración con Frontend

El frontend está en el repositorio **RUTALOCAL1V**.

**Cliente HTTP del frontend:** `lib/api.ts`
- Ya tiene todos los endpoints implementados
- Usa formato de respuesta estándar
- Manejo de errores incluido

**Formato de respuesta esperado:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Mensaje opcional"
}
```

---

## 📞 Soporte

Para dudas sobre implementación:
1. Revisar [README_ACTUALIZACION.md](README_ACTUALIZACION.md)
2. Consultar [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)
3. Ver especificaciones en [BACKEND_README.md](BACKEND_README.md)

---

## 📜 Licencia

Este proyecto es parte de Ruta Local.

---

**Desarrollado con ❤️ para conectar a turistas con negocios locales de Santiago** 🇨🇱
