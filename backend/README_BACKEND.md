# 🔧 Backend API - Ruta Local

API REST completa para la plataforma Ruta Local, construida con Django REST Framework.

## 📋 Tabla de Contenidos

- [Stack Tecnológico](#stack-tecnológico)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Endpoints Disponibles](#endpoints-disponibles)
- [Desarrollo](#desarrollo)
- [Testing](#testing)
- [Deployment](#deployment)

## 💻 Stack Tecnológico

- **Framework:** Django 5.0 + Django REST Framework 3.14
- **Base de Datos:** PostgreSQL 15+
- **Autenticación:** JWT (Simple JWT)
- **Cache:** Redis (opcional)
- **Storage:** Cloudinary / AWS S3
- **Task Queue:** Celery (opcional)

## 🚀 Instalación

### Requisitos Previos

- Python 3.10+
- PostgreSQL 15+
- pip y virtualenv

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd backend
```

2. **Crear entorno virtual**
```bash
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements/development.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Crear base de datos**
```bash
# En PostgreSQL
createdb rutalocal_dev
```

6. **Ejecutar migraciones**
```bash
python manage.py migrate
```

7. **Crear superusuario**
```bash
python manage.py createsuperuser
```

8. **Cargar datos de ejemplo**
```bash
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/features.json
```

9. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

## ⚙️ Configuración

### Variables de Entorno (.env)

Copiar `.env.example` a `.env` y configurar:

```bash
# Django
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=rutalocal_dev
DB_USER=postgres
DB_PASSWORD=tu-password
DB_HOST=localhost
DB_PORT=5432

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60  # minutos
JWT_REFRESH_TOKEN_LIFETIME=10080  # 7 días

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Servicios Externos
MAPBOX_ACCESS_TOKEN=tu-token-mapbox
GOOGLE_CLIENT_ID=tu-client-id
GOOGLE_CLIENT_SECRET=tu-client-secret
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
```

## 📁 Estructura del Proyecto

```
backend/
├── apps/                           # Aplicaciones Django
│   ├── authentication/            # Auth y usuarios
│   │   ├── models.py             # Modelo User extendido
│   │   ├── serializers.py        # Serializers de auth
│   │   ├── views.py              # Vistas de auth
│   │   └── urls.py
│   │
│   ├── businesses/                # Negocios locales
│   │   ├── models.py             # Business, Category, Feature
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── admin.py
│   │   └── urls.py
│   │
│   ├── routes/                    # Rutas personalizadas
│   │   ├── models.py             # Route, RouteStop
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── reviews/                   # Reviews y ratings
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
│
├── config/                        # Configuración Django
│   ├── settings/
│   │   ├── base.py               # Settings base
│   │   ├── development.py        # Settings desarrollo
│   │   └── production.py         # Settings producción
│   ├── urls.py
│   └── wsgi.py
│
├── core/                          # Utils compartidos
│   ├── exceptions.py             # Exception handlers
│   └── pagination.py
│
├── fixtures/                      # Datos de ejemplo
│   ├── categories.json
│   └── features.json
│
├── requirements/                  # Dependencias
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
│
├── manage.py
├── .env.example
└── README_BACKEND.md
```

## 🔌 Endpoints Disponibles

### Autenticación (`/api/auth/`)

- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `POST /api/auth/google` - Login con Google OAuth
- `GET /api/auth/me` - Usuario actual
- `POST /api/auth/refresh` - Refrescar token

### Negocios (`/api/businesses/`)

- `GET /api/businesses/` - Listar negocios (con filtros)
- `GET /api/businesses/<slug>/` - Detalle de negocio
- `POST /api/businesses/<id>/favorite/` - Agregar a favoritos
- `DELETE /api/businesses/<id>/unfavorite/` - Quitar de favoritos
- `POST /api/businesses/<id>/visit/` - Registrar visita

### Categorías (`/api/businesses/`)

- `GET /api/businesses/categories/` - Listar categorías

### Rutas (`/api/routes/`)

- `GET /api/routes/` - Listar rutas del usuario
- `POST /api/routes/create/` - Crear nueva ruta
- `GET /api/routes/<id>/` - Detalle de ruta
- `PUT /api/routes/<id>/update/` - Actualizar ruta
- `DELETE /api/routes/<id>/delete/` - Eliminar ruta
- `POST /api/routes/<id>/like/` - Dar like
- `DELETE /api/routes/<id>/unlike/` - Quitar like

### Reviews (`/api/`)

- `GET /api/businesses/<id>/reviews/` - Listar reviews de un negocio
- `POST /api/businesses/<id>/reviews/create/` - Crear review
- `PUT /api/reviews/<id>/update/` - Actualizar review
- `DELETE /api/reviews/<id>/delete/` - Eliminar review
- `POST /api/reviews/<id>/helpful/` - Marcar como útil

### Formato de Respuesta

Todas las respuestas siguen el formato:

```json
{
  "success": true,
  "data": { ... },
  "message": "Mensaje opcional"
}
```

En caso de error:

```json
{
  "success": false,
  "message": "Error description",
  "errors": { ... }
}
```

## 🛠️ Desarrollo

### Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar shell interactivo
python manage.py shell

# Cargar datos de ejemplo
python manage.py loaddata fixtures/categories.json

# Ejecutar tests
python manage.py test

# O con pytest
pytest
```

### Admin Panel

Acceder al panel de administración en: `http://localhost:8000/admin`

### Crear Nueva App

```bash
python manage.py startapp nombre_app apps/nombre_app
```

## 🧪 Testing

Ejecutar todos los tests:

```bash
python manage.py test
```

Con pytest:

```bash
pytest
```

Con coverage:

```bash
pytest --cov=apps --cov-report=html
```

## 📦 Deployment

### Preparar para Producción

1. **Actualizar settings de producción**
```python
# config/settings/production.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com']
```

2. **Recolectar archivos estáticos**
```bash
python manage.py collectstatic --no-input
```

3. **Ejecutar migraciones**
```bash
python manage.py migrate --settings=config.settings.production
```

### Con Gunicorn

```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Con Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements/production.txt .
RUN pip install -r production.txt

COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 📝 Notas Importantes

### PostGIS (Opcional)

Para habilitar búsquedas geoespaciales avanzadas:

1. Instalar PostGIS en PostgreSQL
2. Cambiar `DB_ENGINE` a `django.contrib.gis.db.backends.postgis`
3. En la base de datos ejecutar: `CREATE EXTENSION postgis;`
4. Actualizar el modelo `Business` para usar `PointField` en lugar de `latitude/longitude`

### Google OAuth

Para configurar Google OAuth:

1. Crear proyecto en Google Cloud Console
2. Habilitar Google+ API
3. Crear credenciales OAuth 2.0
4. Agregar `http://localhost:3000/auth/google/callback` como redirect URI
5. Copiar Client ID y Secret al .env

### Mapbox API

Para funcionalidades de mapa:

1. Crear cuenta en Mapbox
2. Obtener Access Token
3. Agregar token al .env

## 🐛 Troubleshooting

### Error de conexión a PostgreSQL

```bash
# Verificar que PostgreSQL está corriendo
psql -U postgres -l

# Crear base de datos si no existe
createdb rutalocal_dev
```

### Error de migraciones

```bash
# Resetear migraciones (CUIDADO: borra datos)
python manage.py migrate --fake app_name zero
python manage.py migrate app_name
```

### Error de CORS

Verificar que el frontend URL está en `CORS_ALLOWED_ORIGINS` en el .env

## 📞 Soporte

Para más información, consultar:
- [BACKEND_REQUIREMENTS.md](../BACKEND_REQUIREMENTS.md) - Especificaciones completas
- [Django REST Framework Docs](https://www.django-rest-framework.org/)
- [Django Docs](https://docs.djangoproject.com/)

## ✅ Checklist de Desarrollo

**FASE 1 - MVP:**
- [x] Setup de proyecto Django
- [x] Modelos de User, Business, Category, Feature
- [x] Auth: Register, Login, JWT
- [x] Businesses: List, Detail, Search
- [x] Filtros básicos
- [x] CORS configurado
- [ ] Deploy básico

**FASE 2 - Features Core:**
- [x] Rutas: CRUD completo
- [x] Reviews: CRUD básico
- [x] Favorites: Add/Remove
- [ ] Dashboard con stats
- [ ] Google OAuth completo
- [ ] Rate limiting
- [ ] Tests unitarios

**FASE 3 - Engagement:**
- [ ] Sistema de likes
- [ ] Notificaciones
- [ ] Email notifications
- [ ] Recommendations engine
- [ ] Error tracking con Sentry

**FASE 4 - Optimización:**
- [ ] Caché con Redis
- [ ] Celery tasks
- [ ] Optimización de queries
- [ ] Tests completos
- [ ] CI/CD pipeline
- [ ] Documentación API con Swagger

---

**Última actualización:** Diciembre 7, 2025
**Versión:** 1.0.0
