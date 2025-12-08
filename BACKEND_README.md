# 🗺️ Ruta Local - Backend Integration Guide

**Documentación completa para desarrollar el backend de Ruta Local**

Este documento contiene toda la información necesaria para crear el backend que se integre perfectamente con el frontend de Ruta Local.

---

## 📋 Tabla de Contenidos

1. [Resumen del Proyecto](#resumen-del-proyecto)
2. [Stack Tecnológico Frontend](#stack-tecnológico-frontend)
3. [Arquitectura de Integración](#arquitectura-de-integración)
4. [Modelos de Datos Requeridos](#modelos-de-datos-requeridos)
5. [Endpoints de API](#endpoints-de-api)
6. [Autenticación y Seguridad](#autenticación-y-seguridad)
7. [Formato de Respuestas](#formato-de-respuestas)
8. [Variables de Entorno](#variables-de-entorno)
9. [Casos de Uso](#casos-de-uso)
10. [Datos de Ejemplo](#datos-de-ejemplo)
11. [Stack Recomendado](#stack-recomendado)

---

## 🎯 Resumen del Proyecto

### ¿Qué es Ruta Local?

**Ruta Local** es una plataforma que conecta turistas y locales con emprendimientos auténticos en Santiago de Chile. Los usuarios pueden:

- 🗺️ Explorar negocios locales en un mapa interactivo 3D
- 🔍 Buscar con filtros avanzados (categoría, rating, distancia, precio)
- 🛤️ Crear rutas personalizadas visitando múltiples negocios
- ⭐ Escribir reviews y calificaciones
- ❤️ Guardar favoritos
- 📊 Ver estadísticas en su dashboard personal

### Estado Actual

✅ **Frontend:** 100% completo y funcional
- Next.js 16 con App Router
- TypeScript estricto
- UI moderna con shadcn/ui
- Mapa 3D con Mapbox GL
- Sistema de autenticación implementado
- Cliente HTTP listo para integración

⏳ **Backend:** Pendiente de desarrollo
- Todos los endpoints están documentados
- Formatos de respuesta definidos
- Integración lista para conectar

---

## 💻 Stack Tecnológico Frontend

### Framework y Lenguaje
```
Next.js 16.0.7 (App Router)
React 19.2.0
TypeScript 5.9.3
```

### UI y Estilos
```
Tailwind CSS 4.1.9
shadcn/ui (Radix UI + Tailwind)
Lucide Icons
Framer Motion (animaciones)
```

### Mapas
```
Mapbox GL JS 3.17.0
React Map GL 8.1.0
PostGIS (esperado en backend)
```

### Estado y Autenticación
```
React Context API
localStorage para persistencia
JWT tokens (esperado del backend)
```

### Deployment
```
Frontend: Vercel
URL Producción: https://v0-hero-section-for-ruta-local.vercel.app
```

---

## 🏗️ Arquitectura de Integración

### Estructura del Frontend

```
RUTALOCAL1V/
├── app/                          # Next.js App Router
│   ├── (routes)/
│   │   ├── login/               # Login page
│   │   ├── register/            # Register page
│   │   ├── dashboard/           # User dashboard
│   │   ├── map-interactive/     # Mapa 3D Mapbox
│   │   └── builder/             # Constructor de rutas
│   └── api/                     # API routes (Next.js)
│
├── components/                   # Componentes React
│   ├── ui/                      # shadcn/ui components
│   ├── dashboard/               # Dashboard components
│   ├── map/                     # Mapa components
│   │   ├── mapbox-map.tsx
│   │   ├── map-search-bar.tsx
│   │   └── business-carousel.tsx
│   └── route-builder/
│
├── contexts/
│   ├── auth-context.tsx         # ⚡ Manejo de autenticación
│   └── filter-context.tsx       # Estado de filtros
│
├── lib/
│   ├── api.ts                   # 🔥 Cliente HTTP para backend
│   ├── env.ts                   # Variables de entorno
│   ├── auth/                    # Servicios de autenticación
│   │   ├── auth.service.ts
│   │   ├── token-manager.ts
│   │   └── types.ts
│   └── mapbox-data.ts           # Datos mock de negocios
│
└── .env.example                 # Template de configuración
```

### Cliente HTTP Implementado

El frontend ya tiene un **cliente HTTP completo** en `lib/api.ts`:

```typescript
// lib/api.ts
import { env, apiRoutes } from './env'

class ApiClient {
  private baseUrl: string = env.apiEndpoint
  
  private getHeaders(includeAuth = true): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    }
    
    if (includeAuth) {
      const token = this.getToken()
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }
    }
    
    return headers
  }
  
  async get<T>(url: string): Promise<T>
  async post<T>(url: string, data: unknown): Promise<T>
  async put<T>(url: string, data: unknown): Promise<T>
  async delete<T>(url: string): Promise<T>
}

// Exports listos para usar
export const authApi = {
  login: (email, password) => { ... },
  register: (name, email, password) => { ... },
  logout: () => { ... },
  getCurrentUser: () => { ... },
}

export const businessApi = {
  list: (filters) => { ... },
  getById: (id) => { ... },
  search: (query) => { ... },
}

export const routeApi = {
  list: () => { ... },
  create: (data) => { ... },
  update: (id, data) => { ... },
}
```

### URLs de API Configurables

```typescript
// lib/env.ts
export const env = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  apiBasePath: process.env.NEXT_PUBLIC_API_BASE_PATH || '/api',
  
  get apiEndpoint() {
    return `${this.apiUrl}${this.apiBasePath}`
  }
}

// Rutas de API predefinidas
export const apiRoutes = {
  auth: {
    login: `${env.apiEndpoint}/auth/login`,
    register: `${env.apiEndpoint}/auth/register`,
    logout: `${env.apiEndpoint}/auth/logout`,
    me: `${env.apiEndpoint}/auth/me`,
    google: `${env.apiEndpoint}/auth/google`,
  },
  businesses: {
    list: `${env.apiEndpoint}/businesses`,
    detail: (id) => `${env.apiEndpoint}/businesses/${id}`,
    search: `${env.apiEndpoint}/businesses/search`,
  },
  routes: {
    list: `${env.apiEndpoint}/routes`,
    detail: (id) => `${env.apiEndpoint}/routes/${id}`,
  }
}
```

---

## 📊 Modelos de Datos Requeridos

### 1. User (Usuario)

```typescript
interface User {
  id: string                    // UUID
  email: string                 // Único
  name: string
  password: string              // Hasheado
  avatar?: string               // URL de imagen
  
  // OAuth
  google_id?: string            // ID de Google
  
  // Preferencias
  preferred_language: string    // 'es', 'en'
  notifications_enabled: boolean
  
  // Estadísticas
  routes_created: number
  businesses_visited: number
  
  // Timestamps
  created_at: Date
  updated_at: Date
  last_login_at?: Date
}
```

### 2. Business (Negocio Local)

```typescript
interface Business {
  id: string                    // UUID
  name: string
  slug: string                  // URL-friendly
  description: string
  short_description: string     // Max 200 chars
  
  // Categorización
  category_id: string           // FK a Category
  category: Category
  tags: string[]
  
  // Contacto
  phone: string
  email?: string
  website?: string
  instagram?: string
  
  // Geolocalización (PostGIS Point)
  location: {
    type: 'Point'
    coordinates: [number, number]  // [lng, lat]
  }
  lat: number                   // -33.4372
  lng: number                   // -70.6506
  address: string
  neighborhood: string          // "Lastarria", "Bellavista"
  comuna: string                // "Santiago Centro"
  
  // Horarios
  hours: {
    monday: { open: string, close: string }
    tuesday: { open: string, close: string }
    // ... resto de días
  }
  is_open_24h: boolean
  
  // Características
  features: string[]            // ["WiFi", "Terraza", "Pet-friendly"]
  price_range: 1 | 2 | 3 | 4    // $, $$, $$$, $$$$
  
  // Media
  images: string[]              // URLs
  cover_image: string
  logo?: string
  
  // Ratings
  rating: number                // 0.0 - 5.0
  review_count: number
  verified: boolean             // Verificado por Ruta Local
  
  // Stats
  views: number
  favorites_count: number
  visits_count: number
  
  // Status
  is_active: boolean
  is_featured: boolean
  
  // Timestamps
  created_at: Date
  updated_at: Date
}
```

### 3. Category (Categoría)

```typescript
interface Category {
  id: string
  name: string                  // "Café", "Restaurante"
  slug: string
  icon: string                  // Nombre de icono Lucide
  color: string                 // Hex color
  description?: string
  order: number                 // Para ordenar en UI
  is_active: boolean
}

// Categorías requeridas:
const CATEGORIES = [
  { name: 'Café', icon: 'coffee', color: '#8B4513' },
  { name: 'Restaurante', icon: 'utensils', color: '#E74C3C' },
  { name: 'Bar/Pub', icon: 'beer', color: '#F39C12' },
  { name: 'Galería', icon: 'palette', color: '#9B59B6' },
  { name: 'Tienda', icon: 'shopping-bag', color: '#3498DB' },
  { name: 'Librería', icon: 'book', color: '#2ECC71' },
  { name: 'Teatro', icon: 'theater', color: '#E91E63' },
  { name: 'Hostal', icon: 'bed', color: '#00BCD4' },
  { name: 'Mercado', icon: 'shopping-cart', color: '#FF5722' },
  { name: 'Artesanía', icon: 'scissors', color: '#795548' },
  { name: 'Panadería', icon: 'croissant', color: '#FFC107' },
  { name: 'Heladería', icon: 'ice-cream', color: '#E91E63' },
]
```

### 4. Route (Ruta Personalizada)

```typescript
interface Route {
  id: string
  user_id: string               // FK a User
  user: User
  
  // Info
  name: string
  description?: string
  
  // Configuración
  is_public: boolean
  is_featured: boolean
  
  // Stats calculados
  total_distance: number        // En km
  estimated_duration: number    // En minutos
  stops_count: number
  
  // Engagement
  views: number
  likes: number
  
  // Timestamps
  created_at: Date
  updated_at: Date
}
```

### 5. RouteStop (Parada de Ruta)

```typescript
interface RouteStop {
  id: string
  route_id: string              // FK a Route
  business_id: string           // FK a Business
  business: Business
  
  // Orden
  order: number                 // 1, 2, 3...
  
  // Tiempos
  duration: number              // Minutos en el lugar
  notes?: string                // Notas del usuario
  
  // Completado
  is_completed: boolean
  completed_at?: Date
}
```

### 6. Review (Reseña)

```typescript
interface Review {
  id: string
  user_id: string               // FK a User
  business_id: string           // FK a Business
  user: User
  
  // Rating
  rating: 1 | 2 | 3 | 4 | 5
  
  // Contenido
  title?: string
  comment: string
  would_recommend: boolean
  
  // Media
  images: string[]
  
  // Engagement
  helpful_count: number
  
  // Status
  is_verified_visit: boolean
  is_approved: boolean
  
  // Timestamps
  created_at: Date
  updated_at: Date
}

// CONSTRAINT: Un usuario solo puede hacer 1 review por negocio
```

### 7. Favorite (Favorito)

```typescript
interface Favorite {
  id: string
  user_id: string               // FK a User
  business_id: string           // FK a Business
  created_at: Date
}

// CONSTRAINT: Unique (user_id, business_id)
```

### 8. Visit (Visita Registrada)

```typescript
interface Visit {
  id: string
  user_id: string               // FK a User
  business_id: string           // FK a Business
  route_id?: string             // FK a Route (opcional)
  
  visited_at: Date
  notes?: string
}
```

---

## 🔌 Endpoints de API

### Base URL

```
Desarrollo: http://localhost:8000/api
Producción: https://api.rutalocal.com/api
```

### 1. Autenticación (`/api/auth/`)

#### `POST /api/auth/register`

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
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "juan@example.com",
      "name": "Juan Pérez",
      "avatar": null,
      "routes_created": 0,
      "businesses_visited": 0
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "Usuario registrado exitosamente"
}
```

**Errores (400):**
```json
{
  "success": false,
  "message": "Error de validación",
  "errors": {
    "email": ["Este email ya está registrado"],
    "password": ["La contraseña debe tener al menos 8 caracteres"]
  }
}
```

#### `POST /api/auth/login`

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
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "juan@example.com",
      "name": "Juan Pérez",
      "avatar": "https://...",
      "routes_created": 5,
      "businesses_visited": 23
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

#### `POST /api/auth/google`

Login con Google OAuth.

**Request:**
```json
{
  "token": "google-oauth-id-token"
}
```

**Response:** Mismo formato que `/login`

#### `GET /api/auth/me`

Obtener usuario actual (requiere autenticación).

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "juan@example.com",
    "name": "Juan Pérez",
    "avatar": "https://...",
    "routes_created": 5,
    "businesses_visited": 23,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### `POST /api/auth/logout`

Cerrar sesión (requiere autenticación).

**Response (200):**
```json
{
  "success": true,
  "message": "Sesión cerrada exitosamente"
}
```

---

### 2. Negocios (`/api/businesses/`)

#### `GET /api/businesses/`

Listar negocios con filtros avanzados.

**Query Parameters:**
- `category` - Slug de categoría (ej: `cafe`)
- `neighborhood` - Barrio (ej: `Lastarria`)
- `lat` & `lng` - Coordenadas para búsqueda por distancia
- `radius` - Radio en km (default: 5)
- `rating_min` - Rating mínimo (0-5)
- `price_range` - Rango de precio (1-4)
- `features` - Features separadas por coma (ej: `wifi,terraza`)
- `is_open` - Solo negocios abiertos (`true`/`false`)
- `search` - Búsqueda por nombre o descripción
- `page` - Número de página (default: 1)
- `per_page` - Items por página (default: 20, max: 100)
- `sort` - Campo de ordenamiento (`rating`, `distance`, `name`)
- `order` - Orden (`asc` o `desc`)

**Ejemplo:**
```
GET /api/businesses/?category=cafe&lat=-33.4372&lng=-70.6506&radius=2&rating_min=4.5&features=wifi,terraza&page=1&per_page=20
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Café Literario",
        "slug": "cafe-literario",
        "short_description": "Café con ambiente acogedor y libros",
        "category": {
          "id": "cat-001",
          "name": "Café",
          "slug": "cafe",
          "icon": "coffee",
          "color": "#8B4513"
        },
        "location": {
          "lat": -33.4372,
          "lng": -70.6386
        },
        "address": "Lastarria 305, Santiago Centro",
        "neighborhood": "Lastarria",
        "comuna": "Santiago Centro",
        "phone": "+56 2 2633 5432",
        "website": "https://cafeliterario.cl",
        "instagram": "@cafeliterario",
        "rating": 4.8,
        "review_count": 234,
        "price_range": 2,
        "distance": 0.5,
        "cover_image": "https://cloudinary.com/...",
        "images": ["https://...", "https://..."],
        "features": ["WiFi", "Terraza", "Libros"],
        "is_open": true,
        "closes_at": "22:00",
        "verified": true,
        "is_featured": false,
        "hours": {
          "monday": { "open": "08:00", "close": "22:00" },
          "tuesday": { "open": "08:00", "close": "22:00" }
        }
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 156,
      "pages": 8,
      "has_next": true,
      "has_prev": false
    },
    "filters_applied": {
      "category": "cafe",
      "radius": 2,
      "rating_min": 4.5,
      "features": ["wifi", "terraza"]
    }
  }
}
```

#### `GET /api/businesses/:id`

Obtener detalle completo de un negocio.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Café Literario",
    "slug": "cafe-literario",
    "description": "Descripción completa del negocio con historia y detalles...",
    "short_description": "Café con ambiente acogedor y libros",
    "category": { /* ... */ },
    "location": { "lat": -33.4372, "lng": -70.6386 },
    "address": "Lastarria 305, Santiago Centro",
    "neighborhood": "Lastarria",
    "phone": "+56 2 2633 5432",
    "email": "info@cafeliterario.cl",
    "website": "https://cafeliterario.cl",
    "instagram": "@cafeliterario",
    "hours": { /* ... */ },
    "features": [
      { "name": "WiFi", "icon": "wifi" },
      { "name": "Terraza", "icon": "sun" }
    ],
    "price_range": 2,
    "rating": 4.8,
    "review_count": 234,
    "images": ["https://...", "https://..."],
    "cover_image": "https://...",
    "logo": "https://...",
    "verified": true,
    "is_featured": false,
    "views": 1234,
    "favorites_count": 89,
    "visits_count": 567,
    "recent_reviews": [
      /* 3 reviews más recientes */
    ],
    "similar_businesses": [
      /* 4 negocios similares */
    ],
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-12-01T15:20:00Z"
  }
}
```

#### `GET /api/businesses/search`

Búsqueda de negocios por nombre o descripción.

**Query Parameters:**
- `q` - Query de búsqueda
- `lat` & `lng` - Coordenadas opcionales
- `page` - Número de página

**Ejemplo:**
```
GET /api/businesses/search?q=cafe+literario&lat=-33.4372&lng=-70.6506
```

**Response:** Mismo formato que `/api/businesses/`

#### `POST /api/businesses/:id/favorite`

Agregar negocio a favoritos (requiere autenticación).

**Headers:**
```
Authorization: Bearer {token}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Negocio agregado a favoritos"
}
```

#### `DELETE /api/businesses/:id/favorite`

Quitar negocio de favoritos (requiere autenticación).

**Response (200):**
```json
{
  "success": true,
  "message": "Negocio quitado de favoritos"
}
```

#### `POST /api/businesses/:id/visit`

Registrar visita a un negocio (requiere autenticación).

**Request:**
```json
{
  "route_id": "optional-route-id",
  "notes": "¡Excelente café!"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Visita registrada",
  "data": {
    "visit_id": "visit-001",
    "visited_at": "2024-12-08T15:30:00Z"
  }
}
```

---

### 3. Categorías (`/api/categories/`)

#### `GET /api/categories/`

Listar todas las categorías activas.

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "cat-001",
      "name": "Café",
      "slug": "cafe",
      "icon": "coffee",
      "color": "#8B4513",
      "description": "Cafeterías y cafés locales",
      "business_count": 45,
      "order": 1
    },
    {
      "id": "cat-002",
      "name": "Restaurante",
      "slug": "restaurante",
      "icon": "utensils",
      "color": "#E74C3C",
      "business_count": 89,
      "order": 2
    }
  ]
}
```

---

### 4. Rutas (`/api/routes/`)

#### `GET /api/routes/`

Listar rutas del usuario autenticado.

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
- `is_public` - Filtrar por públicas/privadas
- `page` - Número de página

**Response (200):**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "route-001",
        "name": "Tour Gastronómico Lastarria",
        "description": "Recorrido por los mejores lugares de Lastarria",
        "stops_count": 5,
        "total_distance": 2.3,
        "estimated_duration": 180,
        "is_public": true,
        "is_featured": false,
        "likes": 23,
        "views": 456,
        "created_at": "2024-12-01T10:00:00Z",
        "updated_at": "2024-12-05T14:30:00Z",
        "preview_businesses": [
          {
            "id": "bus-001",
            "name": "Café Literario",
            "cover_image": "https://..."
          },
          {
            "id": "bus-002",
            "name": "Galería NAC",
            "cover_image": "https://..."
          }
        ]
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 5,
      "pages": 1
    }
  }
}
```

#### `GET /api/routes/:id`

Obtener detalle completo de una ruta.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "route-001",
    "name": "Tour Gastronómico Lastarria",
    "description": "Recorrido por los mejores lugares de Lastarria",
    "user": {
      "id": "user-001",
      "name": "Juan Pérez",
      "avatar": "https://..."
    },
    "stops": [
      {
        "id": "stop-001",
        "order": 1,
        "duration": 60,
        "notes": "Probar el flat white",
        "is_completed": false,
        "business": {
          "id": "bus-001",
          "name": "Café Literario",
          "location": { "lat": -33.4372, "lng": -70.6386 },
          "cover_image": "https://...",
          "category": { "name": "Café", "icon": "coffee" },
          "rating": 4.8
        }
      },
      {
        "id": "stop-002",
        "order": 2,
        "duration": 90,
        "notes": "",
        "is_completed": false,
        "business": { /* ... */ }
      }
    ],
    "total_distance": 2.3,
    "estimated_duration": 180,
    "is_public": true,
    "is_featured": false,
    "views": 456,
    "likes": 23,
    "created_at": "2024-12-01T10:00:00Z",
    "updated_at": "2024-12-05T14:30:00Z"
  }
}
```

#### `POST /api/routes/`

Crear nueva ruta (requiere autenticación).

**Headers:**
```
Authorization: Bearer {token}
```

**Request:**
```json
{
  "name": "Tour Gastronómico Lastarria",
  "description": "Recorrido por los mejores lugares",
  "is_public": false,
  "stops": [
    {
      "business_id": "bus-001",
      "order": 1,
      "duration": 60,
      "notes": "Probar el flat white"
    },
    {
      "business_id": "bus-002",
      "order": 2,
      "duration": 90,
      "notes": "Ver la exposición"
    }
  ]
}
```

**Response (201):**
```json
{
  "success": true,
  "data": { /* Ruta completa */ },
  "message": "Ruta creada exitosamente"
}
```

**Validaciones:**
- Mínimo 2 stops
- Todos los `business_id` deben existir
- `order` debe ser consecutivo (1, 2, 3...)
- `duration` debe ser > 0

#### `PUT /api/routes/:id`

Actualizar ruta (requiere autenticación + ownership).

**Request:** Mismo formato que POST

**Response (200):**
```json
{
  "success": true,
  "data": { /* Ruta actualizada */ },
  "message": "Ruta actualizada exitosamente"
}
```

#### `DELETE /api/routes/:id`

Eliminar ruta (requiere autenticación + ownership).

**Response (200):**
```json
{
  "success": true,
  "message": "Ruta eliminada exitosamente"
}
```

#### `POST /api/routes/:id/like`

Dar like a una ruta (requiere autenticación).

**Response (201):**
```json
{
  "success": true,
  "message": "Like agregado",
  "data": {
    "likes": 24
  }
}
```

#### `DELETE /api/routes/:id/like`

Quitar like (requiere autenticación).

**Response (200):**
```json
{
  "success": true,
  "message": "Like quitado",
  "data": {
    "likes": 23
  }
}
```

---

### 5. Reviews (`/api/reviews/`)

#### `GET /api/businesses/:business_id/reviews`

Listar reviews de un negocio.

**Query Parameters:**
- `rating` - Filtrar por rating (1-5)
- `page` - Número de página
- `per_page` - Items por página

**Response (200):**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "review-001",
        "user": {
          "id": "user-001",
          "name": "Juan Pérez",
          "avatar": "https://..."
        },
        "rating": 5,
        "title": "Excelente café",
        "comment": "El mejor café de Lastarria. Ambiente acogedor y atención de primera.",
        "would_recommend": true,
        "images": ["https://...", "https://..."],
        "helpful_count": 12,
        "is_verified_visit": true,
        "created_at": "2024-12-01T10:00:00Z",
        "updated_at": "2024-12-01T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 234,
      "pages": 12
    },
    "stats": {
      "average_rating": 4.8,
      "total_reviews": 234,
      "rating_distribution": {
        "5": 180,
        "4": 40,
        "3": 10,
        "2": 3,
        "1": 1
      },
      "would_recommend_percentage": 95.3
    }
  }
}
```

#### `POST /api/businesses/:business_id/reviews`

Crear review (requiere autenticación).

**Headers:**
```
Authorization: Bearer {token}
```

**Request:**
```json
{
  "rating": 5,
  "title": "Excelente café",
  "comment": "El mejor café de Lastarria...",
  "would_recommend": true,
  "images": [
    "base64-encoded-image-1",
    "base64-encoded-image-2"
  ]
}
```

**Response (201):**
```json
{
  "success": true,
  "data": { /* Review completo */ },
  "message": "Review creado exitosamente"
}
```

**Validaciones:**
- Usuario no puede tener más de 1 review por negocio
- Rating debe ser 1-5
- Comment mínimo 10 caracteres
- Máximo 5 imágenes

#### `PUT /api/reviews/:id`

Actualizar review (requiere autenticación + ownership).

#### `DELETE /api/reviews/:id`

Eliminar review (requiere autenticación + ownership).

#### `POST /api/reviews/:id/helpful`

Marcar review como útil (requiere autenticación).

**Response (201):**
```json
{
  "success": true,
  "message": "Marcado como útil",
  "data": {
    "helpful_count": 13
  }
}
```

---

### 6. Usuario (`/api/users/`)

#### `GET /api/users/me`

Perfil del usuario actual (requiere autenticación).

**Response:** Mismo que `/api/auth/me`

#### `PUT /api/users/me`

Actualizar perfil (requiere autenticación).

**Request:**
```json
{
  "name": "Juan Pérez García",
  "phone": "+56912345678",
  "avatar": "base64-encoded-image",
  "preferred_language": "es",
  "notifications_enabled": true
}
```

**Response (200):**
```json
{
  "success": true,
  "data": { /* Usuario actualizado */ },
  "message": "Perfil actualizado exitosamente"
}
```

#### `GET /api/users/me/favorites`

Negocios favoritos del usuario.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "results": [
      { /* Business completo */ }
    ],
    "pagination": { /* ... */ }
  }
}
```

#### `GET /api/users/me/routes`

Rutas del usuario.

**Response:** Mismo que `/api/routes/`

#### `GET /api/users/me/reviews`

Reviews escritas por el usuario.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "review-001",
        "business": {
          "id": "bus-001",
          "name": "Café Literario",
          "cover_image": "https://..."
        },
        "rating": 5,
        "title": "Excelente café",
        "comment": "...",
        "created_at": "2024-12-01T10:00:00Z"
      }
    ],
    "pagination": { /* ... */ }
  }
}
```

#### `GET /api/users/me/visits`

Historial de visitas del usuario.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "visit-001",
        "business": {
          "id": "bus-001",
          "name": "Café Literario",
          "cover_image": "https://..."
        },
        "route": {
          "id": "route-001",
          "name": "Tour Gastronómico"
        },
        "visited_at": "2024-12-05T15:30:00Z",
        "notes": "¡Excelente!"
      }
    ],
    "pagination": { /* ... */ }
  }
}
```

#### `GET /api/users/me/dashboard`

Datos para el dashboard del usuario.

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
      "total_distance": 45.6,
      "total_time": 1234
    },
    "recent_routes": [
      /* 3 rutas más recientes */
    ],
    "recent_visits": [
      /* 5 visitas más recientes */
    ],
    "recommendations": [
      /* 6 negocios recomendados */
    ],
    "activity_chart": [
      { "month": "Enero", "visits": 5, "reviews": 2 },
      { "month": "Febrero", "visits": 8, "reviews": 3 }
    ]
  }
}
```

---

## 🔐 Autenticación y Seguridad

### JWT Tokens

**Estructura del Token:**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "juan@example.com",
  "iat": 1702034567,
  "exp": 1702038167
}
```

**Duración:**
- Access Token: 1 hora
- Refresh Token: 7 días

**Headers de Autenticación:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Refresh Token Flow

```
1. Access token expira (401)
2. Frontend usa refresh token
3. POST /api/auth/refresh
4. Backend valida refresh token
5. Retorna nuevo access token
6. Frontend reintenta request original
```

### Password Requirements

```
- Mínimo 8 caracteres
- Al menos 1 mayúscula
- Al menos 1 número
- Caracteres especiales permitidos
```

### Rate Limiting

```
Auth endpoints: 5 requests/minuto
Business list: 60 requests/minuto
Create route: 10 requests/hora
Create review: 5 requests/hora
```

### CORS

**Desarrollo:**
```
http://localhost:3000
http://127.0.0.1:3000
```

**Producción:**
```
https://v0-hero-section-for-ruta-local.vercel.app
https://rutalocal.com
https://www.rutalocal.com
```

---

## 📝 Formato de Respuestas

### Respuesta Exitosa

```json
{
  "success": true,
  "data": { /* ... */ },
  "message": "Operación exitosa"
}
```

### Error de Validación (400)

```json
{
  "success": false,
  "message": "Error de validación",
  "errors": {
    "email": ["Este campo es requerido", "Email inválido"],
    "password": ["La contraseña debe tener al menos 8 caracteres"]
  }
}
```

### Error de Autenticación (401)

```json
{
  "success": false,
  "message": "No autenticado",
  "errors": {
    "auth": ["Token inválido o expirado"]
  }
}
```

### Error de Permisos (403)

```json
{
  "success": false,
  "message": "No tienes permiso para realizar esta acción"
}
```

### Not Found (404)

```json
{
  "success": false,
  "message": "Recurso no encontrado"
}
```

### Error del Servidor (500)

```json
{
  "success": false,
  "message": "Error interno del servidor",
  "error_id": "err-12345"
}
```

### Paginación

```json
{
  "success": true,
  "data": {
    "results": [ /* ... */ ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 156,
      "pages": 8,
      "has_next": true,
      "has_prev": false,
      "next_url": "/api/businesses/?page=2",
      "prev_url": null
    }
  }
}
```

---

## ⚙️ Variables de Entorno

### Backend (.env)

```bash
# ===========================================
# Django Settings
# ===========================================
DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# ===========================================
# Database (PostgreSQL + PostGIS)
# ===========================================
DB_ENGINE=django.contrib.gis.db.backends.postgis
DB_NAME=rutalocal_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# ===========================================
# Redis (Cache)
# ===========================================
REDIS_URL=redis://localhost:6379/0

# ===========================================
# JWT
# ===========================================
JWT_SECRET_KEY=super-secret-jwt-key-change-in-production
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080

# ===========================================
# CORS
# ===========================================
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://v0-hero-section-for-ruta-local.vercel.app

# ===========================================
# Google OAuth
# ===========================================
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx

# ===========================================
# Mapbox
# ===========================================
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ

# ===========================================
# Cloudinary (Image Storage)
# ===========================================
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# ===========================================
# SendGrid (Emails)
# ===========================================
SENDGRID_API_KEY=SG.xxx
DEFAULT_FROM_EMAIL=noreply@rutalocal.com

# ===========================================
# Sentry (Error Tracking)
# ===========================================
SENTRY_DSN=https://xxx@sentry.io/xxx

# ===========================================
# Frontend URL
# ===========================================
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local)

```bash
# Backend Django
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_PATH=/api

# Modo desarrollo (aceptar cualquier credencial)
NEXT_PUBLIC_DEV_MODE=false

# Storage keys
NEXT_PUBLIC_STORAGE_KEY=santiago_user
NEXT_PUBLIC_TOKEN_KEY=santiago_token

# Mapbox
NEXT_PUBLIC_MAPBOX_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ

# Google OAuth
NEXT_PUBLIC_GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx

# App URL
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## 💡 Casos de Uso

### 1. Usuario Explora Negocios en Mapa

```
1. Usuario abre /map-interactive
2. Frontend obtiene geolocalización del navegador
3. GET /api/businesses/?lat=-33.4372&lng=-70.6506&radius=5
4. Backend usa PostGIS para búsqueda geoespacial
5. Retorna negocios ordenados por distancia
6. Frontend renderiza marcadores en Mapbox
```

### 2. Usuario Aplica Filtros

```
1. Usuario selecciona:
   - Categoría: "Café"
   - Rating mínimo: 4.5
   - Features: WiFi, Terraza
2. GET /api/businesses/?category=cafe&rating_min=4.5&features=wifi,terraza
3. Backend aplica filtros con Django Q objects
4. Retorna resultados filtrados
5. Frontend actualiza mapa y listado
```

### 3. Usuario Crea Ruta

```
1. Usuario busca y selecciona 3+ negocios
2. Organiza orden con drag & drop
3. POST /api/routes/ con:
   {
     "name": "Tour Lastarria",
     "stops": [
       { "business_id": "A", "order": 1, "duration": 60 },
       { "business_id": "B", "order": 2, "duration": 90 }
     ]
   }
4. Backend:
   - Valida negocios
   - Calcula distancia total usando Mapbox API
   - Estima duración
   - Guarda ruta
5. Retorna ruta completa
6. Frontend redirige a /dashboard
```

### 4. Usuario Escribe Review

```
1. Usuario visita negocio y click "Escribir reseña"
2. Completa formulario:
   - Rating: 5 estrellas
   - Comentario: "Excelente café..."
   - Sube 2 fotos
3. Frontend sube imágenes a Cloudinary
4. POST /api/businesses/:id/reviews con URLs
5. Backend:
   - Valida que user no tenga review previa
   - Guarda review
   - Recalcula rating promedio del negocio
   - Incrementa review_count
6. Retorna review creado
7. Frontend muestra toast de éxito
```

### 5. Login con Google OAuth

```
1. Usuario click "Continuar con Google"
2. Frontend abre popup OAuth de Google
3. Usuario autoriza
4. Google redirige con token
5. POST /api/auth/google con token
6. Backend:
   - Valida token con Google API
   - Obtiene email y perfil
   - Busca usuario por google_id o email
   - Si no existe, crea nuevo usuario
   - Genera JWT tokens
7. Retorna user + tokens
8. Frontend guarda en localStorage y redirige
```

---

## 📦 Datos de Ejemplo

### Seed de Categorías

```sql
INSERT INTO categories (id, name, slug, icon, color, "order") VALUES
('cat-001', 'Café', 'cafe', 'coffee', '#8B4513', 1),
('cat-002', 'Restaurante', 'restaurante', 'utensils', '#E74C3C', 2),
('cat-003', 'Bar/Pub', 'bar-pub', 'beer', '#F39C12', 3),
('cat-004', 'Galería', 'galeria', 'palette', '#9B59B6', 4),
('cat-005', 'Tienda', 'tienda', 'shopping-bag', '#3498DB', 5),
('cat-006', 'Librería', 'libreria', 'book', '#2ECC71', 6),
('cat-007', 'Teatro', 'teatro', 'theater', '#E91E63', 7),
('cat-008', 'Hostal', 'hostal', 'bed', '#00BCD4', 8),
('cat-009', 'Mercado', 'mercado', 'shopping-cart', '#FF5722', 9),
('cat-010', 'Artesanía', 'artesania', 'scissors', '#795548', 10),
('cat-011', 'Panadería', 'panaderia', 'croissant', '#FFC107', 11),
('cat-012', 'Heladería', 'heladeria', 'ice-cream', '#E91E63', 12);
```

### Seed de Features

```sql
INSERT INTO features (name, slug, icon, category) VALUES
('WiFi', 'wifi', 'wifi', 'amenity'),
('Terraza', 'terraza', 'sun', 'amenity'),
('Pet-friendly', 'pet-friendly', 'dog', 'amenity'),
('Accesible', 'accesible', 'accessibility', 'accessibility'),
('Reservas', 'reservas', 'calendar', 'service'),
('Delivery', 'delivery', 'truck', 'service'),
('Take Away', 'take-away', 'shopping-bag', 'service'),
('Estacionamiento', 'estacionamiento', 'parking', 'amenity'),
('Eventos', 'eventos', 'calendar-days', 'service'),
('Live Music', 'live-music', 'music', 'amenity');
```

### Seed de Negocios (Ejemplos)

```python
# 50 negocios distribuidos por Santiago
SEED_BUSINESSES = [
    {
        "name": "Café Literario",
        "slug": "cafe-literario",
        "category": "cafe",
        "lat": -33.4372,
        "lng": -70.6386,
        "neighborhood": "Lastarria",
        "comuna": "Santiago Centro",
        "address": "Lastarria 305",
        "phone": "+56 2 2633 5432",
        "rating": 4.8,
        "price_range": 2,
        "verified": True,
        "features": ["wifi", "terraza", "pet-friendly"],
    },
    {
        "name": "Galería NAC",
        "slug": "galeria-nac",
        "category": "galeria",
        "lat": -33.4368,
        "lng": -70.6392,
        "neighborhood": "Lastarria",
        "comuna": "Santiago Centro",
        "address": "Morandé 361",
        "phone": "+56 2 2664 9620",
        "rating": 4.6,
        "price_range": 1,
        "verified": True,
        "features": ["accesible", "eventos"],
    },
    # ... 48 negocios más
]
```

### Coordenadas de Barrios

```python
NEIGHBORHOODS = {
    "Lastarria": (-33.4372, -70.6386),
    "Bellavista": (-33.4291, -70.6390),
    "Providencia": (-33.4260, -70.6100),
    "Barrio Italia": (-33.4450, -70.6280),
    "Las Condes": (-33.4080, -70.5730),
    "Ñuñoa": (-33.4569, -70.5967),
    "Santiago Centro": (-33.4410, -70.6517),
}
```

---

## 🛠️ Stack Recomendado

### Opción 1: Django (Recomendado)

**Stack:**
```
Django 5.0+
Django REST Framework 3.14+
PostgreSQL 15+ con PostGIS
Redis 7+
Celery (tareas asíncronas)
```

**Pros:**
- Ecosistema maduro
- GeoDjango para queries geoespaciales
- Admin panel incluido
- ORM potente
- Seguridad robusta

**Dependencias:**
```bash
pip install django djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install psycopg2-binary
pip install django-filter
pip install celery redis
pip install cloudinary
pip install google-auth
pip install sentry-sdk
```

### Opción 2: FastAPI (Alternativa)

**Stack:**
```
FastAPI 0.104+
SQLAlchemy 2.0+
PostgreSQL 15+ con PostGIS
Redis 7+
Celery
```

**Pros:**
- Performance superior
- Async/await nativo
- Auto-documentación con Swagger
- Tipado moderno

**Dependencias:**
```bash
pip install fastapi uvicorn
pip install sqlalchemy geoalchemy2
pip install psycopg2-binary
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install python-multipart
pip install redis celery
pip install cloudinary
pip install google-auth
pip install sentry-sdk
```

### Base de Datos

**PostgreSQL con PostGIS:**
```sql
-- Crear base de datos
CREATE DATABASE rutalocal_dev;

-- Conectar y activar PostGIS
\c rutalocal_dev
CREATE EXTENSION postgis;

-- Verificar instalación
SELECT PostGIS_version();
```

### Deployment

**Recomendaciones:**

1. **Railway** (Más fácil)
   - Deploy automático desde GitHub
   - PostgreSQL + PostGIS incluido
   - Redis incluido
   - $5-20/mes

2. **Render**
   - Similar a Railway
   - Free tier disponible
   - Buen soporte para Django/FastAPI

3. **AWS (EC2 + RDS)**
   - Más control
   - Escalable
   - Más complejo
   - $30-100/mes

---

## 📚 Recursos Adicionales

### Documentación del Frontend

```
RUTALOCAL1V/
├── README.md                    # Overview del proyecto
├── BACKEND_INTEGRATION.md       # Guía rápida de integración
├── BACKEND_REQUIREMENTS.md      # Especificaciones detalladas
├── ENV_SETUP.md                 # Configuración de variables
├── LOGIN_IMPLEMENTATION.md      # Sistema de autenticación
├── MAPA_INTERACTIVO.md          # Especificaciones del mapa
└── ROADMAP.md                   # Plan de desarrollo
```

### Archivos Clave

**Cliente HTTP:**
```
lib/api.ts              - Cliente HTTP con todos los endpoints
lib/env.ts              - Variables de entorno tipadas
lib/auth/               - Servicios de autenticación
```

**Contextos:**
```
contexts/auth-context.tsx    - Estado global de autenticación
contexts/filter-context.tsx  - Estado de filtros del mapa
```

**Componentes:**
```
components/map/              - Componentes del mapa 3D
components/dashboard/        - Dashboard del usuario
components/route-builder/    - Constructor de rutas
```

### Testing del Backend

**Endpoints a probar:**
```bash
# Health check
curl http://localhost:8000/api/health

# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","password":"Test123!"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!"}'

# List businesses
curl http://localhost:8000/api/businesses/?lat=-33.4372&lng=-70.6506

# Get business detail
curl http://localhost:8000/api/businesses/{id}
```

---

## 🚀 Pasos para Empezar

### Checklist Backend Developer

1. **Setup Inicial**
   - [ ] Clonar repositorio frontend (para referencia)
   - [ ] Revisar documentación completa
   - [ ] Configurar PostgreSQL + PostGIS localmente
   - [ ] Crear estructura de proyecto

2. **Base de Datos**
   - [ ] Crear modelos (User, Business, Category, etc.)
   - [ ] Configurar PostGIS para geolocalización
   - [ ] Crear migraciones
   - [ ] Seed de datos iniciales

3. **Autenticación**
   - [ ] Implementar JWT tokens
   - [ ] Endpoints: register, login, me, logout
   - [ ] Middleware de autenticación
   - [ ] Google OAuth

4. **API Core**
   - [ ] CRUD de negocios
   - [ ] Búsqueda con filtros
   - [ ] Queries geoespaciales
   - [ ] Paginación

5. **Features**
   - [ ] Sistema de rutas
   - [ ] Reviews y ratings
   - [ ] Favoritos
   - [ ] Dashboard con stats

6. **Integración**
   - [ ] CORS configurado
   - [ ] Variables de entorno
   - [ ] Probar con frontend
   - [ ] Deploy

---

## 📞 Soporte y Contacto

### En caso de dudas:

1. Revisar documentación del frontend
2. Consultar ejemplos en `lib/api.ts`
3. Verificar formatos de respuesta esperados
4. Probar endpoints con Postman/Thunder Client

### URLs Importantes

**Frontend:**
- Desarrollo: http://localhost:3000
- Producción: https://v0-hero-section-for-ruta-local.vercel.app
- Repo: RUTALOCAL1V

**Backend Esperado:**
- Desarrollo: http://localhost:8000
- Base path: /api
- Docs: /api/docs (Swagger)

---

## ✅ Resumen Ejecutivo

### El Backend DEBE Entregar:

✅ **Autenticación completa** (JWT + Google OAuth)
✅ **CRUD de negocios** con búsqueda geoespacial
✅ **Sistema de rutas** con cálculo de distancias
✅ **Reviews y ratings**
✅ **Dashboard** con estadísticas
✅ **API REST** siguiendo endpoints documentados
✅ **CORS** configurado para frontend
✅ **Formato de respuestas** consistente

### Frontend está Listo:

✅ Cliente HTTP implementado (`lib/api.ts`)
✅ Variables de entorno configuradas
✅ Interfaces TypeScript definidas
✅ Manejo de errores implementado
✅ UI completa y funcional
✅ Mapa 3D con Mapbox

### Integración:

```typescript
// Frontend solo necesita cambiar:
NEXT_PUBLIC_DEV_MODE=false
NEXT_PUBLIC_API_URL=http://localhost:8000

// Y el backend responderá automáticamente
```

---

**Documento generado:** 8 de Diciembre, 2025
**Versión:** 2.0
**Estado:** Listo para desarrollo backend

---

¡Éxito con el desarrollo! 🚀

Si tienes preguntas, revisa:
- `BACKEND_INTEGRATION.md` - Guía rápida
- `ENV_SETUP.md` - Configuración detallada
- `lib/api.ts` - Cliente HTTP con ejemplos
