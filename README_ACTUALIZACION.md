# 📖 Guía de Actualización del Backend

## ⚠️ URGENTE - Frontend en Producción

**Frontend:** https://rutago-nine.vercel.app/ (✅ ONLINE)  
**Backend:** ⚠️ NO EN PRODUCCIÓN

👉 **Lee primero:** [DEPLOY_URGENTE.md](DEPLOY_URGENTE.md) - Deploy en Railway (1-2 horas)

---

## 🎯 Resumen Rápido

He analizado completamente el frontend (BACKEND_README.md) y el backend actual. He creado:

1. ✅ **Plan de implementación detallado** (`IMPLEMENTATION_PLAN.md`)
2. ✅ **Resumen de cambios** (`BACKEND_UPDATE_SUMMARY.md`)
3. ✅ **Utilidades core** (`backend/core/responses.py` y `backend/core/utils.py`)
4. ✅ **Fixtures de datos** (Categorías y Features)
5. ✅ **Script de setup rápido** (`QUICK_SETUP.bat`)

---

## 🚀 Inicio Rápido

### 1. Cargar Fixtures (INMEDIATO)

```bash
cd backend

# Activar entorno virtual
venv\Scripts\activate

# Cargar categorías y features
python manage.py loaddata fixtures\01_categories.json
python manage.py loaddata fixtures\02_features.json
```

**O usar el script automático:**
```bash
QUICK_SETUP.bat
```

### 2. Ver los Archivos Creados

**Documentación:**
- 📄 `IMPLEMENTATION_PLAN.md` - Plan completo paso a paso
- 📄 `BACKEND_UPDATE_SUMMARY.md` - Resumen y próximos pasos
- 📄 `README_ACTUALIZACION.md` - Este archivo

**Código:**
- 📝 `backend/core/responses.py` - Funciones de respuesta estándar
- 📝 `backend/core/utils.py` - Utilidades (distancias, filtros, etc.)
- 📝 `backend/fixtures/01_categories.json` - 12 categorías
- 📝 `backend/fixtures/02_features.json` - 10 características

---

## 📋 Estado Actual

### ✅ Lo que ya funciona:
- Modelos completos (User, Business, Category, Feature, etc.)
- Autenticación con JWT
- CRUD básico de negocios, rutas, reviews
- CORS configurado
- Admin panel

### ⚠️ Lo que necesita actualización:

**CRÍTICO (hacer primero):**
1. **Formato de respuestas** - Usar `success_response()` y `error_response()`
2. **Filtros avanzados** - Implementar búsqueda por distancia, rating, etc.
3. **Serializers** - Ajustar formato para match con frontend
4. **Dashboard** - Endpoint con estadísticas completas

**IMPORTANTE (hacer después):**
1. Endpoints de likes en rutas
2. Review stats (distribution, etc.)
3. Datos de ejemplo (50+ negocios)
4. Google OAuth completo
5. Rate limiting

---

## 📂 Estructura de Archivos Nuevos

```
SantiaGo_backend/
├── IMPLEMENTATION_PLAN.md         ← Plan detallado de tareas
├── BACKEND_UPDATE_SUMMARY.md      ← Resumen de cambios
├── README_ACTUALIZACION.md        ← Esta guía
├── QUICK_SETUP.bat                ← Script de setup automático
│
└── backend/
    ├── core/
    │   ├── responses.py           ← ✨ NUEVO: Respuestas estándar
    │   └── utils.py               ← ✨ NUEVO: Utilidades comunes
    │
    └── fixtures/
        ├── 01_categories.json     ← ✨ NUEVO: 12 categorías
        └── 02_features.json       ← ✨ NUEVO: 10 features
```

---

## 🔧 Cómo Usar las Nuevas Utilidades

### 1. Formato de Respuestas

**En tus views, importa:**
```python
from core.responses import success_response, error_response, paginated_response
```

**Ejemplos:**

```python
# Respuesta exitosa simple
return success_response(
    data={"user": user_data},
    message="Login exitoso"
)

# Respuesta con error
return error_response(
    message="Error de validación",
    errors={"email": ["Este email ya está registrado"]},
    status=400
)

# Respuesta paginada
return paginated_response(
    queryset=businesses,
    serializer_class=BusinessSerializer,
    request=request,
    message="Negocios obtenidos exitosamente"
)
```

### 2. Utilidades de Distancia

```python
from core.utils import haversine_distance, filter_businesses_by_location

# Calcular distancia entre dos puntos
distance = haversine_distance(
    lon1=-70.6506, lat1=-33.4372,
    lon2=-70.6386, lat2=-33.4372
)

# Filtrar negocios por radio
businesses_nearby = filter_businesses_by_location(
    queryset=Business.objects.all(),
    lat=-33.4372,
    lng=-70.6506,
    radius=5  # km
)
```

### 3. Verificar si Negocio está Abierto

```python
from core.utils import is_business_open_now

is_open, closes_at = is_business_open_now(business)
```

### 4. Calcular Stats de Ruta

```python
from core.utils import calculate_route_stats

stats = calculate_route_stats(route.stops.all())
# Returns: {'total_distance': 2.3, 'estimated_duration': 180, 'stops_count': 5}
```

---

## 📊 Próximos Pasos (Orden Sugerido)

### PASO 1: Actualizar Views (2-3 horas)

Editar archivos existentes para usar las nuevas utilidades:

```bash
# Archivos a editar:
backend/apps/businesses/views.py
backend/apps/routes/views.py
backend/apps/authentication/views.py
backend/apps/reviews/views.py
```

**Cambiar de:**
```python
return Response(serializer.data)
```

**A:**
```python
from core.responses import success_response
return success_response(serializer.data, message="Operación exitosa")
```

### PASO 2: Implementar Filtros (2 horas)

Crear `backend/apps/businesses/filters.py` con todos los filtros requeridos por el frontend.

Ver detalles en `IMPLEMENTATION_PLAN.md` sección "Filtros Avanzados".

### PASO 3: Actualizar Serializers (1-2 horas)

Ajustar serializers para incluir campos calculados:
- `distance`
- `is_open`
- `closes_at`
- `location` como `{"lat": ..., "lng": ...}`

### PASO 4: Dashboard Endpoint (2 horas)

Crear endpoint `/api/users/me/dashboard` con todas las estadísticas.

Ver especificación en `BACKEND_README.md` línea 1309.

### PASO 5: Testing (1 hora)

Probar con Postman/Thunder Client:
```
POST http://localhost:8000/api/auth/register
POST http://localhost:8000/api/auth/login
GET  http://localhost:8000/api/businesses/
GET  http://localhost:8000/api/categories/
```

---

## 🧪 Testing con Frontend

### 1. Configurar Frontend

En el proyecto del frontend (RUTALOCAL1V), editar `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_PATH=/api
NEXT_PUBLIC_DEV_MODE=false  # ← Cambiar a false para usar backend real
```

### 2. Iniciar Ambos Servidores

**Terminal 1 (Backend):**
```bash
cd backend
python manage.py runserver
# http://localhost:8000
```

**Terminal 2 (Frontend):**
```bash
cd ../RUTALOCAL1V
npm run dev
# http://localhost:3000
```

### 3. Probar Flujo Completo

1. Abrir http://localhost:3000
2. Crear cuenta nueva
3. Login
4. Explorar mapa
5. Crear ruta
6. Ver dashboard

---

## 📝 Comandos Útiles

```bash
# Entrar al backend
cd backend

# Activar entorno virtual
venv\Scripts\activate

# Ver migraciones pendientes
python manage.py showmigrations

# Crear y aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Cargar fixtures
python manage.py loaddata fixtures\01_categories.json
python manage.py loaddata fixtures\02_features.json

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

# Acceder a shell de Django
python manage.py shell

# Tests
python manage.py test
```

---

## 📚 Documentación de Referencia

### Archivos Clave

1. **IMPLEMENTATION_PLAN.md**
   - Plan detallado con todas las tareas
   - Modelos requeridos
   - Endpoints especificados
   - Formatos de respuesta

2. **BACKEND_UPDATE_SUMMARY.md**
   - Resumen de cambios
   - Estado actual vs requerido
   - Checklist de validación
   - Comandos útiles

3. **BACKEND_README.md (del frontend)**
   - Especificaciones completas de la API
   - Formatos de request/response
   - Casos de uso
   - Variables de entorno

### Frontend Reference

En el proyecto RUTALOCAL1V:
- `lib/api.ts` - Cliente HTTP con todos los endpoints
- `lib/env.ts` - Configuración de URLs
- `BACKEND_INTEGRATION.md` - Guía de integración

---

## ❓ FAQ

### ¿Por qué crear estos archivos?

Para tener una guía clara de lo que necesita el frontend y poder implementarlo correctamente.

### ¿Debo hacer todos los cambios ahora?

No. Prioriza FASE 1 (formato de respuestas y filtros básicos) para que el frontend funcione. El resto puedes hacerlo gradualmente.

### ¿Cómo pruebo que funciona?

1. Carga los fixtures
2. Crea un usuario de prueba
3. Usa Postman para probar endpoints
4. Configura el frontend para usar el backend
5. Prueba end-to-end

### ¿Qué hacer si algo no funciona?

1. Revisa la consola del backend para errores
2. Verifica que CORS esté configurado
3. Confirma que las variables de entorno están correctas
4. Revisa `IMPLEMENTATION_PLAN.md` para detalles

---

## ✅ Checklist Rápido

Marca lo que ya hayas hecho:

- [ ] Revisar IMPLEMENTATION_PLAN.md
- [ ] Revisar BACKEND_UPDATE_SUMMARY.md
- [ ] Cargar fixtures de categorías
- [ ] Cargar fixtures de features
- [ ] Actualizar views para usar success_response()
- [ ] Implementar filtros avanzados
- [ ] Actualizar serializers
- [ ] Crear endpoint de dashboard
- [ ] Probar con Postman
- [ ] Probar con frontend

---

## 🎉 ¡Listo!

Tienes todo lo necesario para actualizar el backend. Comienza con:

1. ✅ Cargar fixtures: `QUICK_SETUP.bat`
2. 📖 Leer plan: `IMPLEMENTATION_PLAN.md`
3. 🔧 Empezar con FASE 1

**¡Éxito con el desarrollo!** 🚀

---

**Fecha:** 8 de Diciembre, 2025  
**Autor:** GitHub Copilot CLI
