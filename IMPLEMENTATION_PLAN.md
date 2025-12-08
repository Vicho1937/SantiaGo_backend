# 🔧 Plan de Implementación - Actualización Backend Ruta Local

**Fecha:** 8 de Diciembre, 2025  
**Objetivo:** Actualizar backend para cumplir con especificaciones del BACKEND_README.md del frontend

---

## 📋 Estado Actual vs. Requerimientos

### ✅ YA IMPLEMENTADO

**Modelos:**
- ✅ User con campos OAuth (google_id, github_id)
- ✅ Business con todos los campos requeridos
- ✅ Category con icon, color, order
- ✅ Feature con categorías
- ✅ Tag para negocios
- ✅ Favorite (user + business)
- ✅ Visit con notas y route FK

**Apps:**
- ✅ authentication
- ✅ businesses  
- ✅ routes
- ✅ reviews

**Configuración:**
- ✅ Django 5.0 + DRF
- ✅ JWT authentication
- ✅ CORS configurado
- ✅ Settings separados (base, dev, prod)

---

## 🔴 CAMBIOS NECESARIOS

### 1. Actualizar Modelos Según Especificación

#### Business Model - Cambios menores:
```python
# Cambiar de latitude/longitude a location para match con frontend
# El frontend espera:
"location": {
  "lat": -33.4372,
  "lng": -70.6386
}

# Actual en backend: latitude, longitude (OK, solo ajustar serializer)
```

#### Route Model - Verificar/Agregar:
```python
# Debe tener:
- is_public (Boolean)
- is_featured (Boolean) 
- total_distance (Float en km)
- estimated_duration (Int en minutos)
- stops_count (Int)
- views (Int)
- likes (Int)
- shares (Int)
```

#### RouteStop Model - Verificar:
```python
# Debe tener:
- route (FK)
- business (FK)
- order (Int)
- duration (Int en minutos, default 60)
- notes (TextField)
- is_completed (Boolean)
- completed_at (DateTime nullable)
```

#### Review Model - Verificar campos:
```python
# Debe tener:
- user (FK)
- business (FK)
- rating (1-5)
- title (CharField, opcional)
- comment (TextField)
- would_recommend (Boolean)
- images (JSONField lista)
- helpful_count (Int)
- is_verified_visit (Boolean)
- is_approved (Boolean)
- unique_together = ['user', 'business']
```

---

### 2. Endpoints API - Formato de Respuesta

**CRÍTICO:** El frontend espera este formato EXACTO:

```json
{
  "success": true,
  "data": { ... },
  "message": "Mensaje opcional"
}
```

**Errores:**
```json
{
  "success": false,
  "message": "Descripción del error",
  "errors": {
    "field": ["mensaje de error"]
  }
}
```

#### Endpoints a verificar/crear:

**Autenticación:**
- ✅ POST /api/auth/register
- ✅ POST /api/auth/login
- ⚠️  POST /api/auth/google (verificar implementación)
- ✅ GET /api/auth/me
- ✅ POST /api/auth/logout
- ⚠️  POST /api/auth/refresh (verificar)

**Negocios:**
- ✅ GET /api/businesses/ (con filtros)
- ✅ GET /api/businesses/:id
- ⚠️  GET /api/businesses/search (verificar)
- ⚠️  POST /api/businesses/:id/favorite
- ⚠️  DELETE /api/businesses/:id/favorite
- ⚠️  POST /api/businesses/:id/visit

**Categorías:**
- ⚠️  GET /api/categories/ (debe incluir business_count)

**Rutas:**
- ⚠️  GET /api/routes/ (verificar formato)
- ⚠️  GET /api/routes/:id (verificar stops con business data)
- ⚠️  POST /api/routes/ (crear con stops)
- ⚠️  PUT /api/routes/:id
- ⚠️  DELETE /api/routes/:id
- ⚠️  POST /api/routes/:id/like
- ⚠️  DELETE /api/routes/:id/like

**Reviews:**
- ⚠️  GET /api/businesses/:business_id/reviews (con stats)
- ⚠️  POST /api/businesses/:business_id/reviews
- ⚠️  PUT /api/reviews/:id
- ⚠️  DELETE /api/reviews/:id
- ⚠️  POST /api/reviews/:id/helpful

**Usuario:**
- ⚠️  GET /api/users/me
- ⚠️  PUT /api/users/me
- ⚠️  GET /api/users/me/favorites
- ⚠️  GET /api/users/me/routes
- ⚠️  GET /api/users/me/reviews
- ⚠️  GET /api/users/me/visits
- ⚠️  GET /api/users/me/dashboard (estadísticas completas)

---

### 3. Filtros Avanzados para Negocios

El frontend espera estos query parameters:

```
?category=cafe
&neighborhood=Lastarria
&lat=-33.4372
&lng=-70.6506
&radius=5
&rating_min=4.5
&price_range=2
&features=wifi,terraza
&is_open=true
&search=cafe+literario
&page=1
&per_page=20
&sort=rating
&order=desc
```

**Implementar:**
- Filtro por categoría (slug)
- Filtro por barrio
- Búsqueda geoespacial por lat/lng/radius
- Filtro por rating mínimo
- Filtro por price_range
- Filtro por features múltiples
- Filtro por is_open (calcular según hora actual)
- Búsqueda por texto (name + description)
- Paginación
- Ordenamiento

---

### 4. Serializers - Formato Específico

#### BusinessListSerializer (para listado):
```json
{
  "id": "uuid",
  "name": "string",
  "slug": "string",
  "short_description": "string",
  "category": {
    "id": "uuid",
    "name": "string",
    "slug": "string",
    "icon": "string",
    "color": "#hex"
  },
  "location": {
    "lat": float,
    "lng": float
  },
  "address": "string",
  "neighborhood": "string",
  "comuna": "string",
  "phone": "string",
  "website": "string",
  "instagram": "string",
  "rating": float,
  "review_count": int,
  "price_range": int,
  "distance": float,  // calculado
  "cover_image": "url",
  "images": ["url"],
  "features": ["string"],  // solo nombres
  "is_open": boolean,  // calculado
  "closes_at": "HH:MM",  // calculado
  "verified": boolean,
  "is_featured": boolean,
  "hours": { ... }
}
```

#### BusinessDetailSerializer:
- Todo lo anterior +
- `description` completa
- `features` como objetos: `[{"name": "WiFi", "icon": "wifi"}]`
- `recent_reviews`: 3 reviews más recientes
- `similar_businesses`: 4 negocios similares
- `views`, `favorites_count`, `visits_count`

---

### 5. Dashboard Stats

El endpoint `/api/users/me/dashboard` debe retornar:

```json
{
  "success": true,
  "data": {
    "stats": {
      "routes_created": int,
      "businesses_visited": int,
      "reviews_written": int,
      "favorites_count": int,
      "total_distance": float,
      "total_time": int
    },
    "recent_routes": [...],  // 3 rutas más recientes
    "recent_visits": [...],  // 5 visitas más recientes
    "recommendations": [...],  // 6 negocios recomendados
    "activity_chart": [
      { "month": "Enero", "visits": 5, "reviews": 2 },
      ...
    ]
  }
}
```

---

### 6. Fixtures - Datos de Ejemplo

**Crear fixtures para:**

#### Categories (12 categorías):
```json
[
  {"name": "Café", "slug": "cafe", "icon": "coffee", "color": "#8B4513"},
  {"name": "Restaurante", "slug": "restaurante", "icon": "utensils", "color": "#E74C3C"},
  {"name": "Bar/Pub", "slug": "bar-pub", "icon": "beer", "color": "#F39C12"},
  {"name": "Galería", "slug": "galeria", "icon": "palette", "color": "#9B59B6"},
  {"name": "Tienda", "slug": "tienda", "icon": "shopping-bag", "color": "#3498DB"},
  {"name": "Librería", "slug": "libreria", "icon": "book", "color": "#2ECC71"},
  {"name": "Teatro", "slug": "teatro", "icon": "theater", "color": "#E91E63"},
  {"name": "Hostal", "slug": "hostal", "icon": "bed", "color": "#00BCD4"},
  {"name": "Mercado", "slug": "mercado", "icon": "shopping-cart", "color": "#FF5722"},
  {"name": "Artesanía", "slug": "artesania", "icon": "scissors", "color": "#795548"},
  {"name": "Panadería", "slug": "panaderia", "icon": "croissant", "color": "#FFC107"},
  {"name": "Heladería", "slug": "heladeria", "icon": "ice-cream", "color": "#E91E63"}
]
```

#### Features (10 features):
```json
[
  {"name": "WiFi", "slug": "wifi", "icon": "wifi", "category": "amenity"},
  {"name": "Terraza", "slug": "terraza", "icon": "sun", "category": "amenity"},
  {"name": "Pet-friendly", "slug": "pet-friendly", "icon": "dog", "category": "amenity"},
  {"name": "Accesible", "slug": "accesible", "icon": "accessibility", "category": "accessibility"},
  {"name": "Reservas", "slug": "reservas", "icon": "calendar", "category": "service"},
  {"name": "Delivery", "slug": "delivery", "icon": "truck", "category": "service"},
  {"name": "Take Away", "slug": "take-away", "icon": "shopping-bag", "category": "service"},
  {"name": "Estacionamiento", "slug": "estacionamiento", "icon": "parking", "category": "amenity"},
  {"name": "Eventos", "slug": "eventos", "icon": "calendar-days", "category": "service"},
  {"name": "Live Music", "slug": "live-music", "icon": "music", "category": "amenity"}
]
```

#### Businesses (50+ ejemplos):
- Distribuidos en barrios: Lastarria, Bellavista, Providencia, Barrio Italia, Las Condes, Ñuñoa, Santiago Centro
- Con coordenadas reales de Santiago
- Ratings entre 3.5 y 5.0
- Reviews entre 10 y 500

---

### 7. Middleware y Utilidades

**Crear:**
- Custom exception handler para formato de respuestas
- Rate limiting middleware
- CORS headers correctos
- Pagination personalizada

---

### 8. Variables de Entorno

**Verificar .env.example tenga:**
```bash
# Django
DEBUG=True
SECRET_KEY=...
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=rutalocal_dev
DB_USER=postgres
DB_PASSWORD=...
DB_HOST=localhost
DB_PORT=5432

# JWT
JWT_SECRET_KEY=...
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://v0-hero-section-for-ruta-local.vercel.app

# OAuth
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...

# Mapbox
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ

# Cloudinary
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...

# SendGrid
SENDGRID_API_KEY=...
DEFAULT_FROM_EMAIL=noreply@rutalocal.com

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

---

## 🎯 Priorización de Tareas

### FASE 1 - CRÍTICO (HOY)
1. ✅ Revisar y documentar estado actual
2. ⚠️  Actualizar serializers para formato exacto
3. ⚠️  Crear custom exception handler
4. ⚠️  Verificar todos los endpoints
5. ⚠️  Implementar filtros avanzados de negocios
6. ⚠️  Crear fixtures de categorías y features

### FASE 2 - ALTA (MAÑANA)
1. ⚠️  Endpoint de dashboard completo
2. ⚠️  Sistema de likes en rutas
3. ⚠️  Búsqueda por distancia optimizada
4. ⚠️  Review stats en business detail
5. ⚠️  Crear 50+ negocios de ejemplo

### FASE 3 - MEDIA (SIGUIENTE SEMANA)
1. ⚠️  Google OAuth completo
2. ⚠️  Rate limiting
3. ⚠️  Tests unitarios
4. ⚠️  Documentación API con Swagger
5. ⚠️  Deploy en Railway/Render

---

## 📝 Notas de Implementación

### Cálculo de Distancias
Sin PostGIS, usar fórmula Haversine en Python:
```python
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km
```

### Cálculo de is_open
```python
from datetime import datetime

def is_open_now(business):
    now = datetime.now()
    day_name = now.strftime('%A').lower()
    current_time = now.strftime('%H:%M')
    
    if business.is_open_24h:
        return True
    
    if day_name not in business.hours:
        return False
    
    hours = business.hours[day_name]
    return hours['open'] <= current_time <= hours['close']
```

---

## ✅ Checklist de Validación

Antes de considerar completo:

- [ ] Todos los endpoints responden con formato correcto
- [ ] Frontend puede autenticarse exitosamente
- [ ] Listar negocios funciona con todos los filtros
- [ ] Crear ruta funciona end-to-end
- [ ] Reviews se pueden crear y mostrar
- [ ] Dashboard retorna todas las estadísticas
- [ ] Fixtures cargan correctamente
- [ ] CORS permite requests desde frontend
- [ ] Documentación actualizada

---

**Última actualización:** 8 de Diciembre, 2025
