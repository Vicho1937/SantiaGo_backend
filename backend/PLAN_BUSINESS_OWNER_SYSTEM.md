# 🏢 PLAN COMPLETO: Sistema de Propietarios de Negocios

## 📋 RESUMEN EJECUTIVO

Sistema que permite a usuarios convertirse en "Business Owners" con capacidad controlada de crear y gestionar sus negocios locales en RutaLocal.

---

## 🎯 OBJETIVOS

1. **Admin controla permisos**: Decidir qué usuarios pueden crear negocios
2. **Límites configurables**: Admin define cuántos negocios puede crear cada usuario (1 o ilimitado)
3. **Dashboard real**: Usuarios con negocios ven estadísticas reales
4. **Ubicación en mapa**: Al crear negocio, marcar ubicación exacta
5. **Verificación**: Admin puede revisar/aprobar negocios antes de publicar

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### A. MODELO DE PERMISOS (Backend)

```
User (Usuario Base)
  ↓
BusinessOwnerProfile (Extensión del usuario)
  - can_create_businesses: Boolean
  - max_businesses_allowed: Integer (0, 1, 5, 10, -1=ilimitado)
  - businesses_created_count: Integer
  - is_verified_owner: Boolean
  - subscription_tier: String (free, basic, premium)
  - created_at, updated_at
  ↓
Business (Negocios)
  - owner: ForeignKey(User) [Ya existe]
  - status: String (draft, pending_review, published, rejected)
  - created_by_owner: Boolean
  - approved_by: ForeignKey(User, admin)
  - approved_at: DateTime
```

### B. TIPOS DE USUARIOS

1. **Usuario Normal** (por defecto)
   - Solo puede ver negocios
   - Puede marcar favoritos
   - Puede dejar reviews
   - can_create_businesses = False

2. **Business Owner** (otorgado por admin)
   - Puede crear negocios (según límite)
   - Ve dashboard con sus negocios
   - Recibe estadísticas reales
   - can_create_businesses = True
   - max_businesses_allowed = 1, 5, 10, -1

3. **Admin/Staff**
   - Controla todos los permisos
   - Aprueba/rechaza negocios
   - Asigna límites de creación
   - Gestiona todo el sistema

### C. FLUJO DE TRABAJO

```
┌─────────────────────────────────────────────────────────────┐
│                    ADMIN (Django Admin)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │ Asigna permiso a Usuario X    │
              │ - can_create_businesses: True │
              │ - max_businesses_allowed: 3   │
              └───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               USUARIO X (Frontend - Dashboard)               │
│  • Ve botón "Crear Mi Negocio"                              │
│  • Formulario con selector de mapa                           │
│  • Sube: nombre, descripción, categoría, fotos, horarios    │
│  • Selecciona ubicación en mapa interactivo                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │ Negocio creado con status:    │
              │ "pending_review"              │
              └───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ADMIN (Revisa negocio)                    │
│  • Verifica información                                      │
│  • Verifica ubicación en mapa                                │
│  • Aprueba → status: "published"                             │
│  • Rechaza → status: "rejected" (con razón)                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │ Negocio PUBLICADO             │
              │ - Aparece en mapa             │
              │ - Aparece en feed             │
              │ - Búsquedas públicas          │
              └───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│          USUARIO X (Dashboard con estadísticas)              │
│  📊 Mi Negocio: "Café Literario"                            │
│  • 👁️ Vistas: 1,234                                         │
│  • ⭐ Rating: 4.5/5.0 (45 reviews)                          │
│  • ❤️ Favoritos: 89                                         │
│  • 📍 Visitas registradas: 67                               │
│  • 📈 Gráfico de vistas (últimos 30 días)                   │
│  • 💬 Últimas reseñas                                        │
│  • ✏️ Editar información                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📱 COMPONENTES DEL SISTEMA

### 1. BACKEND (Django)

#### Nuevo modelo: BusinessOwnerProfile
```python
class BusinessOwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_create_businesses = models.BooleanField(default=False)
    max_businesses_allowed = models.IntegerField(default=0)
    # -1 = ilimitado, 0 = ninguno, 1+ = límite específico
    
    is_verified_owner = models.BooleanField(default=False)
    subscription_tier = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Gratis'),
            ('basic', 'Básico - 1 negocio'),
            ('standard', 'Estándar - 3 negocios'),
            ('premium', 'Premium - Ilimitado'),
        ],
        default='free'
    )
    
    # Razón social (opcional, para facturación)
    business_name = models.CharField(max_length=255, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def businesses_created_count(self):
        return self.user.owned_businesses.count()
    
    @property
    def can_create_more(self):
        if not self.can_create_businesses:
            return False
        if self.max_businesses_allowed == -1:  # Ilimitado
            return True
        return self.businesses_created_count < self.max_businesses_allowed
    
    @property
    def remaining_slots(self):
        if self.max_businesses_allowed == -1:
            return "Ilimitado"
        return max(0, self.max_businesses_allowed - self.businesses_created_count)
```

#### Modificación al modelo Business (agregar campos)
```python
class Business(models.Model):
    # ... campos existentes ...
    
    # NUEVOS CAMPOS para control
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Borrador'),
            ('pending_review', 'Pendiente de Revisión'),
            ('published', 'Publicado'),
            ('rejected', 'Rechazado'),
        ],
        default='draft'
    )
    
    created_by_owner = models.BooleanField(default=False)
    # True si lo creó un usuario, False si lo creó admin
    
    approved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_businesses'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
```

#### Endpoints API necesarios
```python
# businesses/views.py

# 1. Crear negocio (solo owners con permisos)
POST /api/businesses/create/
Body: {
    name, description, category, latitude, longitude,
    address, phone, images, hours, etc.
}
Permissions: IsAuthenticated + HasBusinessOwnerPermission
Response: Business creado con status='pending_review'

# 2. Listar MIS negocios
GET /api/businesses/my-businesses/
Permissions: IsAuthenticated
Response: Lista de negocios del usuario con stats

# 3. Dashboard de MI negocio
GET /api/businesses/my-businesses/{id}/dashboard/
Permissions: IsOwner
Response: {
    business: {...},
    stats: {
        views: 1234,
        favorites_count: 89,
        visits_count: 67,
        rating: 4.5,
        review_count: 45,
        views_last_30_days: [datos para gráfico],
        recent_reviews: [últimas 5 reviews]
    }
}

# 4. Editar MI negocio
PATCH /api/businesses/my-businesses/{id}/
Body: {campos a actualizar}
Permissions: IsOwner
Note: Si está published, cambios requieren nueva aprobación

# 5. Verificar permisos del usuario
GET /api/users/me/owner-profile/
Response: {
    can_create_businesses: true,
    max_businesses_allowed: 3,
    businesses_created_count: 1,
    can_create_more: true,
    remaining_slots: 2,
    subscription_tier: 'standard'
}
```

### 2. FRONTEND (Next.js)

#### Rutas nuevas
```
/dashboard/my-business          → Lista de mis negocios
/dashboard/my-business/create   → Crear nuevo negocio
/dashboard/my-business/{id}     → Dashboard de negocio específico
/dashboard/my-business/{id}/edit → Editar negocio
```

#### Componentes clave

**A. Botón condicional en navbar**
```tsx
// Solo visible si user.can_create_businesses
{ownerProfile?.can_create_businesses && (
  <Link href="/dashboard/my-business">
    <Button>
      <Store className="w-4 h-4 mr-2" />
      Mi Negocio
    </Button>
  </Link>
)}
```

**B. Formulario de creación con mapa**
```tsx
// components/business/create-business-form.tsx
- Campos: nombre, descripción, categoría, etc.
- MapLocationPicker: Click en mapa para ubicación
- ImageUploader: Subir fotos a Cloudinary
- HoursEditor: Configurar horarios
- Validaciones en tiempo real
- Preview antes de enviar
```

**C. Dashboard de negocio**
```tsx
// app/dashboard/my-business/[id]/page.tsx
<BusinessDashboard>
  <StatsCards>
    <Card title="Vistas" value={1234} icon={Eye} />
    <Card title="Rating" value="4.5/5.0" icon={Star} />
    <Card title="Favoritos" value={89} icon={Heart} />
    <Card title="Visitas" value={67} icon={MapPin} />
  </StatsCards>
  
  <ViewsChart data={viewsLast30Days} />
  
  <RecentReviews reviews={recentReviews} />
  
  <QuickActions>
    <Button>Editar Info</Button>
    <Button>Ver en Mapa</Button>
    <Button>Responder Reviews</Button>
  </QuickActions>
</BusinessDashboard>
```

### 3. ADMIN (Django Admin)

#### Panel de control para admin
```python
# businesses/admin.py

@admin.register(BusinessOwnerProfile)
class BusinessOwnerProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'can_create_businesses', 
        'businesses_created_count',
        'max_businesses_allowed', 
        'remaining_slots',
        'subscription_tier'
    ]
    list_filter = ['can_create_businesses', 'subscription_tier']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    
    actions = [
        'grant_owner_permission',
        'set_limit_1',
        'set_limit_3',
        'set_unlimited',
        'revoke_permissions'
    ]
    
    def grant_owner_permission(self, request, queryset):
        queryset.update(can_create_businesses=True, max_businesses_allowed=1)
    
    def set_unlimited(self, request, queryset):
        queryset.update(max_businesses_allowed=-1)


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'owner',
        'status',
        'created_by_owner',
        'category', 
        'rating',
        'created_at'
    ]
    list_filter = [
        'status', 
        'created_by_owner', 
        'category',
        'verified'
    ]
    
    # Filtro para ver solo negocios pendientes
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.GET.get('pending'):
            return qs.filter(status='pending_review')
        return qs
    
    actions = [
        'approve_businesses',
        'reject_businesses',
        'publish_businesses'
    ]
    
    def approve_businesses(self, request, queryset):
        queryset.update(
            status='published',
            verified=True,
            approved_by=request.user,
            approved_at=timezone.now()
        )
```

---

## 🎁 MODELO DE MONETIZACIÓN (Sugerido)

### Planes de Suscripción

| Plan | Precio | Negocios | Características |
|------|--------|----------|-----------------|
| **Gratis** | $0 | 0 | Solo ver negocios |
| **Básico** | $9.990/mes | 1 | Dashboard básico, estadísticas |
| **Estándar** | $19.990/mes | 3 | + Análisis avanzado |
| **Premium** | $39.990/mes | Ilimitado | + API access, prioridad |

---

## 📊 VENTAJAS DEL MODELO

✅ **Control total del admin**: Decides quién y cuánto
✅ **Escalable**: De 1 negocio a ilimitado
✅ **Monetizable**: Planes de pago claros
✅ **Verificado**: Aprobación manual evita spam
✅ **Dashboard real**: Datos útiles para dueños
✅ **Ubicación precisa**: Selector en mapa
✅ **Profesional**: Sistema serio y confiable

---

## 🚀 FASES DE IMPLEMENTACIÓN

### FASE 1: Base de Permisos (1-2 días)
- [x] Crear modelo BusinessOwnerProfile
- [x] Migración de BD
- [x] Admin panel para asignar permisos
- [x] Middleware/decorador para verificar permisos

### FASE 2: API Backend (2-3 días)
- [x] Endpoint crear negocio
- [x] Endpoint listar MIS negocios
- [x] Endpoint dashboard con stats
- [x] Endpoint editar negocio
- [x] Permissions y validaciones

### FASE 3: Frontend Dashboard (3-4 días)
- [x] Rutas /dashboard/my-business
- [x] Formulario crear negocio con mapa
- [x] Dashboard con estadísticas
- [x] Gráficos de analytics
- [x] Edición de negocio

### FASE 4: Aprobación y Verificación (1-2 días)
- [x] Sistema de estados (draft, pending, published)
- [x] Panel admin para aprobar/rechazar
- [x] Notificaciones al usuario
- [x] Historial de cambios

### FASE 5: Testing y Refinamiento (2 días)
- [x] Pruebas de permisos
- [x] Pruebas de límites
- [x] Pruebas de dashboard
- [x] UX/UI polish

---

## 📋 TOTAL: 9-13 días de desarrollo

