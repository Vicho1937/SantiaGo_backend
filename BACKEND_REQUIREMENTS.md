# 🔧 TOMA DE REQUERIMIENTOS - BACKEND RUTA LOCAL

**Proyecto:** Backend API REST para Ruta Local  
**Frontend:** Next.js 16 con TypeScript (Repositorio: RUTALOCAL1V)  
**Fecha:** 7 de Diciembre, 2025  
**Estado:** Pendiente de implementación

---

## 📋 ÍNDICE

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Stack Tecnológico Recomendado](#stack-tecnológico-recomendado)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Base de Datos - Modelos](#base-de-datos---modelos)
5. [Endpoints de API](#endpoints-de-api)
6. [Autenticación y Seguridad](#autenticación-y-seguridad)
7. [Integración con Frontend](#integración-con-frontend)
8. [Servicios Externos](#servicios-externos)
9. [Configuración y Variables de Entorno](#configuración-y-variables-de-entorno)
10. [Casos de Uso y Flujos](#casos-de-uso-y-flujos)
11. [Priorización de Desarrollo](#priorización-de-desarrollo)
12. [Consideraciones de Producción](#consideraciones-de-producción)

---

## 🎯 RESUMEN EJECUTIVO

### Objetivo
Desarrollar una API REST completa para **Ruta Local**, plataforma que conecta turistas y locales con emprendimientos auténticos en Santiago de Chile, permitiendo la creación de rutas personalizadas.

### Alcance del Backend
- Sistema de autenticación completo (Email/Password + OAuth)
- Gestión de usuarios y perfiles
- CRUD de negocios locales con geolocalización
- Sistema de rutas personalizadas con drag & drop
- Sistema de reviews y ratings
- Búsqueda avanzada con filtros geoespaciales
- Dashboard con estadísticas y analytics
- Sistema de favoritos y guardados
- Notificaciones (email y push)

### Modelo de Integración
- **Desarrollo:** Backend y Frontend en repositorios separados
- **Producción:** Ambos proyectos unidos pero manteniendo separación lógica
- **Comunicación:** API REST con JSON
- **Base URL:** Frontend espera backend en `http://localhost:8000/api` (desarrollo)

---

## 💻 STACK TECNOLÓGICO RECOMENDADO

### Framework Principal
```
✅ Django 5.0+ con Django REST Framework
```

**Justificación:**
- Ecosistema maduro y robusto
- Excelente soporte para geolocalización (GeoDjango)
- ORM potente con migraciones automáticas
- Admin panel incluido para gestión
- Seguridad incorporada (CSRF, XSS, SQL Injection)

**Alternativa:** FastAPI + SQLAlchemy (si se prefiere async/await)

### Base de Datos
```
✅ PostgreSQL 15+ con PostGIS
```

**Justificación:**
- PostGIS para queries geoespaciales (búsquedas por distancia)
- Soporte nativo para índices GIN/GiST
- JSON fields para datos flexibles
- Escalabilidad probada

### Autenticación
```
✅ JWT (JSON Web Tokens)
   - djangorestframework-simplejwt
   - OAuth 2.0 con Google
```

### Caché y Performance
```
✅ Redis
   - Caché de sesiones
   - Rate limiting
   - Caché de búsquedas frecuentes
```

### Storage de Archivos
```
✅ AWS S3 o Cloudinary
   - Imágenes de negocios
   - Fotos de perfil
   - Assets de rutas
```

### Servicios Adicionales
```
- Celery + Redis (tareas asíncronas)
- SendGrid o AWS SES (emails)
- Mapbox API (geocoding y rutas)
- Sentry (error tracking)
```

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### Estructura de Carpetas Sugerida

```
backend/
├── config/                      # Configuración Django
│   ├── settings/
│   │   ├── base.py             # Settings comunes
│   │   ├── development.py      # Development
│   │   └── production.py       # Production
│   ├── urls.py
│   └── wsgi.py
│
├── apps/                        # Aplicaciones Django
│   ├── authentication/         # Auth y usuarios
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── services.py         # Lógica de negocio
│   │
│   ├── businesses/             # Negocios locales
│   │   ├── models.py           # Business, Category, Feature
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── filters.py          # django-filter para búsquedas
│   │   └── services.py         # Lógica de geolocalización
│   │
│   ├── routes/                 # Rutas personalizadas
│   │   ├── models.py           # Route, RouteStop
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── services.py         # Cálculo de distancias
│   │
│   ├── reviews/                # Reviews y ratings
│   │   ├── models.py
│   │   ├── serializers.py
│   │   └── views.py
│   │
│   └── notifications/          # Sistema de notificaciones
│       ├── models.py
│       ├── tasks.py            # Celery tasks
│       └── services.py
│
├── core/                       # Utils compartidos
│   ├── permissions.py
│   ├── pagination.py
│   ├── exceptions.py
│   └── validators.py
│
├── tests/                      # Tests unitarios e integración
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
│
├── manage.py
├── .env.example
└── README.md
```

---

## 🗄️ BASE DE DATOS - MODELOS

### 1. User (Extendido de AbstractUser)

```python
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models

class User(AbstractUser):
    """Usuario extendido con campos personalizados"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.URLField(blank=True)
    
    # OAuth providers
    google_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
    github_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
    
    # Preferencias
    preferred_language = models.CharField(max_length=10, default='es')
    notifications_enabled = models.BooleanField(default=True)
    
    # Stats
    routes_created = models.IntegerField(default=0)
    businesses_visited = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
```

### 2. Business (Negocios Locales)

```python
class Business(models.Model):
    """Negocios locales de Santiago"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    
    # Info básica
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200)
    
    # Categorización
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    subcategory = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    
    # Contacto y ubicación
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    
    # Geolocalización (PostGIS)
    location = gis_models.PointField()
    address = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=100)  # Lastarria, Bellavista, etc.
    comuna = models.CharField(max_length=100)
    
    # Horarios
    hours = models.JSONField(default=dict)  # { "monday": {"open": "09:00", "close": "18:00"} }
    is_open_24h = models.BooleanField(default=False)
    
    # Características
    features = models.ManyToManyField('Feature')  # WiFi, Terraza, Pet-friendly
    price_range = models.IntegerField(choices=[
        (1, '$'),
        (2, '$$'),
        (3, '$$$'),
        (4, '$$$$'),
    ])
    
    # Media
    images = models.JSONField(default=list)  # URLs de imágenes
    cover_image = models.URLField()
    logo = models.URLField(blank=True)
    
    # Ratings y verificación
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)  # Verificado por Ruta Local
    claimed = models.BooleanField(default=False)   # Reclamado por el dueño
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    
    # Stats
    views = models.IntegerField(default=0)
    favorites_count = models.IntegerField(default=0)
    visits_count = models.IntegerField(default=0)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['category', 'neighborhood']),
            models.Index(fields=['rating', '-created_at']),
            gis_models.Index(fields=['location']),  # Spatial index
        ]
        ordering = ['-rating', '-review_count']
```

### 3. Category (Categorías)

```python
class Category(models.Model):
    """Categorías de negocios"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50)  # Nombre del icono Lucide
    color = models.CharField(max_length=7, default='#000000')  # Hex color
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
```

**Categorías del Frontend:**
- Café
- Restaurante
- Bar/Pub
- Galería
- Tienda
- Librería
- Teatro
- Hostal
- Mercado
- Artesanía
- Panadería
- Heladería

### 4. Feature (Características)

```python
class Feature(models.Model):
    """Características de los negocios"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=[
        ('amenity', 'Amenidad'),
        ('accessibility', 'Accesibilidad'),
        ('payment', 'Métodos de Pago'),
        ('service', 'Servicio'),
    ])
```

**Features del Frontend:**
- WiFi
- Terraza
- Pet-friendly
- Accesible
- Reservas
- Delivery
- Take Away
- Estacionamiento
- Eventos
- Live Music

### 5. Route (Rutas Personalizadas)

```python
class Route(models.Model):
    """Rutas creadas por usuarios"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routes')
    
    # Info básica
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Configuración
    is_public = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Stats calculados
    total_distance = models.FloatField(default=0)  # En km
    estimated_duration = models.IntegerField(default=0)  # En minutos
    stops_count = models.IntegerField(default=0)
    
    # Engagement
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
```

### 6. RouteStop (Paradas de Ruta)

```python
class RouteStop(models.Model):
    """Paradas individuales en una ruta"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    
    # Orden en la ruta
    order = models.IntegerField()
    
    # Tiempos estimados
    duration = models.IntegerField(default=60)  # Tiempo en el lugar (minutos)
    notes = models.TextField(blank=True)  # Notas del usuario
    
    # Completado
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['route', 'order']
```

### 7. Review (Reseñas)

```python
class Review(models.Model):
    """Reseñas de negocios"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reviews')
    
    # Rating
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    
    # Contenido
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    
    # Recomendación
    would_recommend = models.BooleanField(default=True)
    
    # Fotos
    images = models.JSONField(default=list)
    
    # Engagement
    helpful_count = models.IntegerField(default=0)
    
    # Status
    is_verified_visit = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'business']
        ordering = ['-created_at']
```

### 8. Favorite (Favoritos)

```python
class Favorite(models.Model):
    """Negocios favoritos de usuarios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'business']
```

### 9. Visit (Visitas registradas)

```python
class Visit(models.Model):
    """Registro de visitas a negocios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, null=True, blank=True, on_delete=models.SET_NULL)
    
    visited_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-visited_at']
```

### 10. Notification (Notificaciones)

```python
class Notification(models.Model):
    """Sistema de notificaciones"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Tipo de notificación
    type = models.CharField(max_length=50, choices=[
        ('new_review', 'Nueva Reseña'),
        ('route_liked', 'Ruta Recibió Like'),
        ('featured', 'Negocio Destacado'),
        ('new_nearby', 'Nuevo Negocio Cercano'),
    ])
    
    # Contenido
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.URLField(blank=True)
    
    # Estado
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🔌 ENDPOINTS DE API

### Formato de Respuesta Estándar

```json
{
  "success": true,
  "data": { ... },
  "message": "Operación exitosa",
  "errors": null
}
```

### 1. AUTENTICACIÓN (`/api/auth/`)

#### `POST /api/auth/register`
Registro de nuevo usuario

**Request:**
```json
{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "password": "SecurePass123!",
  "password_confirmation": "SecurePass123!"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "juan@example.com",
      "name": "Juan Pérez",
      "avatar": null
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "Usuario registrado exitosamente"
}
```

#### `POST /api/auth/login`
Login con email y contraseña

**Request:**
```json
{
  "email": "juan@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "juan@example.com",
      "name": "Juan Pérez",
      "avatar": "https://..."
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

#### `POST /api/auth/google`
Login con Google OAuth

**Request:**
```json
{
  "token": "google-oauth-token"
}
```

#### `POST /api/auth/logout`
Cerrar sesión (requiere autenticación)

**Headers:**
```
Authorization: Bearer {token}
```

#### `GET /api/auth/me`
Obtener usuario actual

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "juan@example.com",
    "name": "Juan Pérez",
    "avatar": "https://...",
    "routes_created": 5,
    "businesses_visited": 12
  }
}
```

#### `POST /api/auth/refresh`
Refrescar token JWT

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 2. NEGOCIOS (`/api/businesses/`)

#### `GET /api/businesses/`
Listar negocios con filtros

**Query Params:**
- `category` - Filtrar por categoría (slug)
- `neighborhood` - Filtrar por barrio
- `lat` & `lng` - Coordenadas para búsqueda por distancia
- `radius` - Radio de búsqueda en km (default: 5)
- `rating_min` - Rating mínimo
- `price_range` - Rango de precio (1-4)
- `features` - IDs de features separados por coma
- `is_open` - Solo negocios abiertos ahora
- `search` - Búsqueda por nombre o descripción
- `page` - Número de página
- `per_page` - Items por página (max: 100)

**Example:**
```
GET /api/businesses/?category=cafe&lat=-33.4372&lng=-70.6506&radius=2&page=1
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "uuid",
        "name": "Café Literario",
        "slug": "cafe-literario",
        "short_description": "Café con ambiente acogedor",
        "category": {
          "id": "uuid",
          "name": "Café",
          "icon": "coffee"
        },
        "location": {
          "lat": -33.4372,
          "lng": -70.6386
        },
        "address": "Lastarria 305, Santiago Centro",
        "neighborhood": "Lastarria",
        "rating": 4.8,
        "review_count": 234,
        "price_range": 2,
        "distance": 0.5,
        "cover_image": "https://...",
        "features": ["WiFi", "Terraza"],
        "is_open": true,
        "closes_at": "22:00",
        "verified": true
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 156,
      "pages": 8
    }
  }
}
```

#### `GET /api/businesses/:id`
Detalle completo de un negocio

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Café Literario",
    "slug": "cafe-literario",
    "description": "Descripción completa del negocio...",
    "category": { ... },
    "location": { ... },
    "address": "...",
    "neighborhood": "Lastarria",
    "phone": "+56 2 2633 5432",
    "email": "info@cafeliterario.cl",
    "website": "https://...",
    "instagram": "@cafeliterario",
    "hours": {
      "monday": { "open": "08:00", "close": "22:00" },
      "tuesday": { "open": "08:00", "close": "22:00" }
    },
    "features": [
      { "name": "WiFi", "icon": "wifi" },
      { "name": "Terraza", "icon": "sun" }
    ],
    "price_range": 2,
    "rating": 4.8,
    "review_count": 234,
    "images": ["https://...", "https://..."],
    "cover_image": "https://...",
    "verified": true,
    "views": 1234,
    "favorites_count": 89,
    "recent_reviews": [ ... ],  // 3 reviews más recientes
    "similar_businesses": [ ... ]  // 4 negocios similares
  }
}
```

#### `GET /api/businesses/search`
Búsqueda de negocios

**Query Params:**
- `q` - Query de búsqueda

**Response:** Mismo formato que `/api/businesses/`

#### `POST /api/businesses/:id/favorite`
Agregar a favoritos (requiere auth)

#### `DELETE /api/businesses/:id/favorite`
Quitar de favoritos (requiere auth)

#### `POST /api/businesses/:id/visit`
Registrar visita (requiere auth)

---

### 3. CATEGORÍAS (`/api/categories/`)

#### `GET /api/categories/`
Listar todas las categorías

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "Café",
      "slug": "cafe",
      "icon": "coffee",
      "color": "#8B4513",
      "business_count": 45
    }
  ]
}
```

---

### 4. RUTAS (`/api/routes/`)

#### `GET /api/routes/`
Listar rutas del usuario (requiere auth)

**Query Params:**
- `is_public` - Filtrar por públicas/privadas
- `page` - Número de página

**Response (200):**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "uuid",
        "name": "Tour por Lastarria",
        "description": "Recorrido cultural por el barrio",
        "stops_count": 5,
        "total_distance": 2.3,
        "estimated_duration": 180,
        "is_public": true,
        "likes": 23,
        "created_at": "2025-12-01T10:00:00Z",
        "preview_businesses": [
          {
            "id": "uuid",
            "name": "Café Literario",
            "cover_image": "https://..."
          }
        ]
      }
    ],
    "pagination": { ... }
  }
}
```

#### `GET /api/routes/:id`
Detalle completo de una ruta

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Tour por Lastarria",
    "description": "...",
    "user": {
      "id": "uuid",
      "name": "Juan Pérez",
      "avatar": "https://..."
    },
    "stops": [
      {
        "id": "uuid",
        "order": 1,
        "duration": 60,
        "notes": "Probar el flat white",
        "business": {
          "id": "uuid",
          "name": "Café Literario",
          "location": { ... },
          "cover_image": "https://..."
        }
      }
    ],
    "total_distance": 2.3,
    "estimated_duration": 180,
    "is_public": true,
    "views": 156,
    "likes": 23,
    "created_at": "2025-12-01T10:00:00Z"
  }
}
```

#### `POST /api/routes/`
Crear nueva ruta (requiere auth)

**Request:**
```json
{
  "name": "Tour por Lastarria",
  "description": "Recorrido cultural",
  "is_public": false,
  "stops": [
    {
      "business_id": "uuid",
      "order": 1,
      "duration": 60,
      "notes": "Probar el flat white"
    },
    {
      "business_id": "uuid",
      "order": 2,
      "duration": 90,
      "notes": ""
    }
  ]
}
```

**Response (201):**
```json
{
  "success": true,
  "data": { ... },  // Ruta completa
  "message": "Ruta creada exitosamente"
}
```

#### `PUT /api/routes/:id`
Actualizar ruta (requiere auth + ownership)

#### `DELETE /api/routes/:id`
Eliminar ruta (requiere auth + ownership)

#### `POST /api/routes/:id/like`
Dar like a una ruta (requiere auth)

#### `DELETE /api/routes/:id/like`
Quitar like (requiere auth)

---

### 5. REVIEWS (`/api/reviews/`)

#### `GET /api/businesses/:business_id/reviews`
Listar reviews de un negocio

**Query Params:**
- `rating` - Filtrar por rating
- `page` - Número de página

**Response (200):**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "uuid",
        "user": {
          "id": "uuid",
          "name": "Juan Pérez",
          "avatar": "https://..."
        },
        "rating": 5,
        "title": "Excelente café",
        "comment": "El mejor café de Lastarria...",
        "would_recommend": true,
        "images": ["https://..."],
        "helpful_count": 12,
        "created_at": "2025-12-01T10:00:00Z"
      }
    ],
    "pagination": { ... },
    "stats": {
      "average_rating": 4.8,
      "total_reviews": 234,
      "rating_distribution": {
        "5": 180,
        "4": 40,
        "3": 10,
        "2": 3,
        "1": 1
      }
    }
  }
}
```

#### `POST /api/businesses/:business_id/reviews`
Crear review (requiere auth)

**Request:**
```json
{
  "rating": 5,
  "title": "Excelente café",
  "comment": "El mejor café de Lastarria...",
  "would_recommend": true,
  "images": ["base64-image-1", "base64-image-2"]
}
```

#### `PUT /api/reviews/:id`
Actualizar review (requiere auth + ownership)

#### `DELETE /api/reviews/:id`
Eliminar review (requiere auth + ownership)

#### `POST /api/reviews/:id/helpful`
Marcar review como útil (requiere auth)

---

### 6. USUARIO (`/api/users/`)

#### `GET /api/users/me`
Perfil del usuario actual (requiere auth)

#### `PUT /api/users/me`
Actualizar perfil (requiere auth)

**Request:**
```json
{
  "name": "Juan Pérez",
  "phone": "+56912345678",
  "avatar": "base64-image",
  "preferred_language": "es",
  "notifications_enabled": true
}
```

#### `GET /api/users/me/favorites`
Negocios favoritos del usuario

#### `GET /api/users/me/routes`
Rutas del usuario

#### `GET /api/users/me/reviews`
Reviews del usuario

#### `GET /api/users/me/visits`
Historial de visitas

#### `GET /api/users/me/dashboard`
Datos del dashboard

**Response (200):**
```json
{
  "success": true,
  "data": {
    "stats": {
      "routes_created": 5,
      "businesses_visited": 23,
      "reviews_written": 8,
      "favorites_count": 15,
      "total_distance": 45.6
    },
    "recent_routes": [ ... ],
    "recent_visits": [ ... ],
    "recommendations": [ ... ]
  }
}
```

---

### 7. NOTIFICACIONES (`/api/notifications/`)

#### `GET /api/notifications/`
Listar notificaciones (requiere auth)

#### `PUT /api/notifications/:id/read`
Marcar como leída (requiere auth)

#### `POST /api/notifications/mark-all-read`
Marcar todas como leídas (requiere auth)

---

## 🔐 AUTENTICACIÓN Y SEGURIDAD

### JWT Token Authentication

**Headers en todas las peticiones autenticadas:**
```
Authorization: Bearer {access_token}
```

**Token Lifecycle:**
- Access Token: 1 hora de duración
- Refresh Token: 7 días de duración
- Rotación automática de refresh tokens

### Permisos y Roles

**Roles:**
- `user` - Usuario normal
- `business_owner` - Dueño de negocio
- `admin` - Administrador

**Niveles de Acceso:**
- Público: Listar negocios, ver detalles, buscar
- Autenticado: Crear rutas, reviews, favoritos
- Owner: Editar/eliminar sus propios recursos
- Admin: Acceso total

### Rate Limiting

```python
# Limits por endpoint
- Auth: 5 req/min
- Businesses (list): 60 req/min
- Routes (create): 10 req/hour
- Reviews (create): 5 req/hour
```

### CORS

**Allowed Origins (Desarrollo):**
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
```

**Allowed Origins (Producción):**
```python
CORS_ALLOWED_ORIGINS = [
    'https://rutalocal.com',
    'https://www.rutalocal.com',
]
```

### Validaciones de Seguridad

- Passwords: Mínimo 8 caracteres, 1 mayúscula, 1 número
- Email: Verificación de formato y unicidad
- SQL Injection: Protección con ORM de Django
- XSS: Sanitización de inputs
- CSRF: Tokens para peticiones POST/PUT/DELETE

---

## 🔗 INTEGRACIÓN CON FRONTEND

### Variables de Entorno del Frontend

El frontend espera estas configuraciones:

```bash
# Backend URL
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_PATH=/api

# Auth
NEXT_PUBLIC_DEV_MODE=false  # Activar cuando backend esté listo
NEXT_PUBLIC_TOKEN_KEY=santiago_token
NEXT_PUBLIC_STORAGE_KEY=santiago_user
```

### Cliente HTTP del Frontend

El frontend ya tiene implementado:

```typescript
// lib/api.ts
import { authApi, businessApi, routeApi } from '@/lib/api'

// Ejemplos de uso:
await authApi.login(email, password)
await businessApi.list({ category: 'cafe' })
await routeApi.create(routeData)
```

### Formato de Errores

El frontend espera este formato:

```json
{
  "success": false,
  "message": "Error en la validación",
  "errors": {
    "email": ["Este email ya está registrado"],
    "password": ["La contraseña es muy débil"]
  }
}
```

---

## 🌐 SERVICIOS EXTERNOS

### 1. Mapbox API

**Uso:**
- Geocoding (convertir direcciones a coordenadas)
- Reverse geocoding
- Cálculo de distancias entre puntos
- Rutas optimizadas

**Endpoints a usar:**
- `https://api.mapbox.com/geocoding/v5/`
- `https://api.mapbox.com/directions/v5/`

### 2. Google OAuth

**Flujo:**
1. Frontend solicita autorización a Google
2. Google redirige con código
3. Frontend envía código al backend
4. Backend valida con Google y crea/login usuario
5. Backend retorna JWT token

**Configuración:**
```python
GOOGLE_CLIENT_ID = 'xxx.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'xxx'
GOOGLE_REDIRECT_URI = 'http://localhost:3000/auth/google/callback'
```

### 3. Cloudinary (Storage)

**Uso:**
- Upload de imágenes de negocios
- Upload de fotos de perfil
- Upload de fotos en reviews
- Transformaciones automáticas (resize, crop)

### 4. SendGrid (Emails)

**Templates necesarios:**
- Welcome email
- Password reset
- Route shared notification
- Weekly digest
- Review notification

### 5. Sentry (Error Tracking)

**Configuración:**
```python
SENTRY_DSN = 'https://xxx@sentry.io/xxx'
```

---

## ⚙️ CONFIGURACIÓN Y VARIABLES DE ENTORNO

### Archivo `.env.example`

```bash
# ===========================================
# DJANGO SETTINGS
# ===========================================
DEBUG=True
SECRET_KEY=django-insecure-development-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# ===========================================
# DATABASE (PostgreSQL + PostGIS)
# ===========================================
DB_ENGINE=django.contrib.gis.db.backends.postgis
DB_NAME=rutalocal_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# ===========================================
# REDIS (Cache y Celery)
# ===========================================
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# ===========================================
# JWT
# ===========================================
JWT_SECRET_KEY=super-secret-jwt-key-change-in-production
JWT_ACCESS_TOKEN_LIFETIME=60  # minutos
JWT_REFRESH_TOKEN_LIFETIME=10080  # 7 días en minutos

# ===========================================
# CORS
# ===========================================
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# ===========================================
# GOOGLE OAUTH
# ===========================================
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback

# ===========================================
# MAPBOX
# ===========================================
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ

# ===========================================
# CLOUDINARY
# ===========================================
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# ===========================================
# SENDGRID
# ===========================================
SENDGRID_API_KEY=SG.xxx
DEFAULT_FROM_EMAIL=noreply@rutalocal.com

# ===========================================
# SENTRY
# ===========================================
SENTRY_DSN=https://xxx@sentry.io/xxx

# ===========================================
# FRONTEND URL
# ===========================================
FRONTEND_URL=http://localhost:3000
```

---

## 📊 CASOS DE USO Y FLUJOS

### Flujo 1: Registro y Login

1. Usuario ingresa email, nombre y password en frontend
2. Frontend valida formato y envía POST a `/api/auth/register`
3. Backend:
   - Valida datos
   - Hashea password con bcrypt
   - Crea usuario en BD
   - Genera JWT tokens
   - Retorna usuario + tokens
4. Frontend guarda token en localStorage
5. Frontend redirige a `/dashboard`

### Flujo 2: Login con Google

1. Usuario hace click en "Continuar con Google"
2. Frontend abre popup de Google OAuth
3. Usuario autoriza la aplicación
4. Google redirige con código de autorización
5. Frontend envía código a `/api/auth/google`
6. Backend:
   - Valida código con Google API
   - Obtiene email y perfil de Google
   - Busca o crea usuario
   - Genera JWT tokens
   - Retorna usuario + tokens
7. Frontend guarda token y redirige a `/dashboard`

### Flujo 3: Búsqueda de Negocios

1. Usuario abre mapa en `/map-interactive`
2. Frontend obtiene geolocalización del navegador
3. Frontend envía GET a `/api/businesses/?lat=-33.4372&lng=-70.6506&radius=5`
4. Backend:
   - Usa PostGIS para búsqueda geoespacial
   - Calcula distancias
   - Aplica filtros
   - Ordena por distancia o rating
   - Retorna lista paginada
5. Frontend renderiza marcadores en mapa Mapbox

### Flujo 4: Filtros Avanzados

1. Usuario selecciona filtros en sidebar:
   - Categoría: "Café"
   - Rating mínimo: 4.5
   - Precio: $$
   - Features: WiFi, Terraza
2. Frontend construye query string
3. Envía GET a `/api/businesses/?category=cafe&rating_min=4.5&price_range=2&features=wifi,terraza`
4. Backend aplica filtros con Django Q objects
5. Retorna resultados filtrados

### Flujo 5: Crear Ruta Personalizada

1. Usuario busca negocios en mapa
2. Hace click en "Agregar a ruta" en 3+ negocios
3. Organiza orden con drag & drop
4. Click en "Guardar ruta"
5. Frontend envía POST a `/api/routes/` con:
   ```json
   {
     "name": "Tour Gastronómico",
     "stops": [
       { "business_id": "uuid1", "order": 1, "duration": 60 },
       { "business_id": "uuid2", "order": 2, "duration": 90 }
     ]
   }
   ```
6. Backend:
   - Valida ownership de negocios
   - Calcula distancia total usando Mapbox
   - Estima duración
   - Guarda ruta
7. Retorna ruta completa
8. Frontend redirige a `/dashboard` mostrando ruta creada

### Flujo 6: Escribir Review

1. Usuario visita negocio
2. Click en "Escribir reseña"
3. Completa formulario:
   - Rating (1-5 estrellas)
   - Título
   - Comentario
   - Fotos (opcional)
4. Frontend sube imágenes a Cloudinary
5. Envía POST a `/api/businesses/:id/reviews` con URLs de imágenes
6. Backend:
   - Valida que user no tenga review previa
   - Guarda review
   - Recalcula rating promedio del negocio
   - Incrementa review_count
   - Envía notificación al dueño (si existe)
7. Retorna review creado
8. Frontend muestra toast de éxito

---

## 🎯 PRIORIZACIÓN DE DESARROLLO

### FASE 1 - MVP (4-6 semanas)

**Objetivo:** API funcional con features esenciales

**Prioridad CRÍTICA:**
- [ ] Setup de proyecto Django + PostgreSQL + PostGIS
- [ ] Modelos: User, Business, Category, Feature
- [ ] Auth: Register, Login, JWT tokens
- [ ] Businesses: List, Detail, Search con geolocalización
- [ ] Filtros básicos (categoría, rating, distancia)
- [ ] CORS configurado
- [ ] Deploy básico en servidor

**Entregables:**
- Frontend puede autenticarse
- Frontend puede listar y buscar negocios
- Mapa funcional con datos reales

### FASE 2 - Features Core (3-4 semanas)

**Prioridad ALTA:**
- [ ] Rutas: CRUD completo
- [ ] RouteStops con cálculo de distancias
- [ ] Reviews: CRUD básico
- [ ] Favorites: Add/Remove
- [ ] Dashboard con stats básicos
- [ ] Google OAuth
- [ ] Rate limiting
- [ ] Tests unitarios básicos

**Entregables:**
- Usuarios pueden crear rutas
- Sistema de reviews funcional
- OAuth con Google

### FASE 3 - Engagement (2-3 semanas)

**Prioridad MEDIA:**
- [ ] Sistema de likes en rutas
- [ ] Notificaciones in-app
- [ ] Email notifications con SendGrid
- [ ] Sistema de visitas registradas
- [ ] Recommendations engine básico
- [ ] Admin panel personalizado
- [ ] Sentry error tracking

**Entregables:**
- Sistema de engagement completo
- Notificaciones funcionando
- Error tracking en producción

### FASE 4 - Optimización (2-3 semanas)

**Prioridad BAJA:**
- [ ] Caché con Redis
- [ ] Celery para tareas asíncronas
- [ ] Optimización de queries
- [ ] Tests de integración completos
- [ ] CI/CD pipeline
- [ ] Documentación API con Swagger
- [ ] Métricas y monitoring

**Entregables:**
- Performance optimizado
- Tests completos
- Documentación API

---

## 🚀 CONSIDERACIONES DE PRODUCCIÓN

### Deployment

**Opciones recomendadas:**
1. **Railway** (Más fácil)
   - Deploy automático desde GitHub
   - PostgreSQL incluido
   - Redis incluido
   - $5-20/mes

2. **DigitalOcean App Platform**
   - Similar a Railway
   - Buen soporte para Django
   - $12-25/mes

3. **AWS (EC2 + RDS + S3)**
   - Más control
   - Más complejo
   - Más escalable
   - $30-100/mes

### Database

**PostgreSQL + PostGIS:**
- Backups automáticos diarios
- Réplicas para lectura
- Connection pooling con PgBouncer
- Índices en campos frecuentes

### Caché

**Redis:**
- Caché de queries comunes
- Rate limiting
- Sesiones de usuario
- Celery broker

### Storage

**Cloudinary o AWS S3:**
- Imágenes optimizadas automáticamente
- CDN incluido
- Transformaciones on-the-fly

### Monitoring

**Herramientas:**
- Sentry (errors)
- New Relic o DataDog (performance)
- Uptime Robot (disponibilidad)
- CloudWatch Logs (AWS)

### Security

**Checklist:**
- [ ] DEBUG=False en producción
- [ ] SECRET_KEY único y seguro
- [ ] HTTPS obligatorio
- [ ] Rate limiting activo
- [ ] SQL injection: protegido con ORM
- [ ] XSS: sanitización de inputs
- [ ] CSRF tokens
- [ ] CORS configurado correctamente
- [ ] Passwords hasheados con bcrypt
- [ ] JWT secrets seguros
- [ ] Environment variables en servidor

### Performance

**Optimizaciones:**
- Queries con select_related / prefetch_related
- Índices en campos de búsqueda
- Pagination en todos los listados
- Compresión gzip
- Static files en CDN
- Database connection pooling

### Backup

**Estrategia:**
- Backups diarios automáticos
- Retención: 30 días
- Backups antes de deploys
- Procedimiento de restore documentado

---

## 📚 DOCUMENTACIÓN ADICIONAL

### Scripts de Migración

```bash
# Crear base de datos
createdb rutalocal_dev

# Activar PostGIS
psql rutalocal_dev -c "CREATE EXTENSION postgis;"

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superuser
python manage.py createsuperuser

# Cargar datos de ejemplo
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/businesses.json
```

### Datos de Seed

Crear 50 negocios de ejemplo basados en:
- 7 barrios: Lastarria, Bellavista, Providencia, etc.
- 12 categorías del frontend
- Coordenadas reales de Santiago
- Features variadas

### Tests

```python
# Estructura de tests
tests/
├── test_auth.py          # Tests de autenticación
├── test_businesses.py    # Tests de negocios
├── test_routes.py        # Tests de rutas
├── test_reviews.py       # Tests de reviews
└── test_geolocation.py   # Tests de búsquedas geoespaciales
```

---

## 📞 CONTACTO Y SIGUIENTES PASOS

### Checklist de Inicio

**Backend Developer debe:**
1. [ ] Revisar este documento completo
2. [ ] Clonar repositorio del frontend para entender integración
3. [ ] Configurar PostgreSQL + PostGIS localmente
4. [ ] Crear estructura de proyecto Django
5. [ ] Implementar modelos básicos
6. [ ] Configurar variables de entorno
7. [ ] Crear endpoints de auth (FASE 1)
8. [ ] Probar integración con frontend

### Reunión de Kick-off

**Temas a definir:**
- Stack final (Django vs FastAPI)
- Cronograma de FASE 1
- Estrategia de deployment
- Acceso a servicios externos (Mapbox, Cloudinary)
- Flujo de trabajo Git
- Code review process

### Recursos

**Frontend:**
- Repo: RUTALOCAL1V
- Docs: BACKEND_INTEGRATION.md, ENV_SETUP.md
- Cliente HTTP: lib/api.ts
- Tipos esperados: lib/api.ts interfaces

**Referencias:**
- Django REST Framework: https://www.django-rest-framework.org/
- PostGIS: https://docs.djangoproject.com/en/5.0/ref/contrib/gis/
- JWT: https://django-rest-framework-simplejwt.readthedocs.io/

---

## ✅ RESUMEN EJECUTIVO

### Lo que el Backend DEBE entregar:

1. **Auth completo** (register, login, JWT, Google OAuth)
2. **CRUD de negocios** con búsqueda geoespacial
3. **CRUD de rutas** con cálculo de distancias
4. **Sistema de reviews** y ratings
5. **Dashboard** con estadísticas
6. **API REST** siguiendo los endpoints definidos
7. **CORS** configurado para frontend
8. **Rate limiting** básico
9. **Error handling** consistente
10. **Deploy funcional** en producción

### Formato de respuesta estándar:
```json
{
  "success": true/false,
  "data": { ... },
  "message": "...",
  "errors": { ... }
}
```

### Headers esperados:
```
Content-Type: application/json
Authorization: Bearer {token}
```

### Frontend está listo y esperando:
- Cliente HTTP configurado (lib/api.ts)
- Variables de entorno definidas (.env.example)
- Interfaces TypeScript para responses
- Manejo de errores implementado

---

**Documento generado:** 7 de Diciembre, 2025  
**Versión:** 1.0  
**Estado:** Listo para desarrollo

¡Éxito con el desarrollo del backend! 🚀
