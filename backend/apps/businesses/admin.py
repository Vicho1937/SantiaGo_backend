from django.contrib import admin
from .models import Business, Category, Feature, Tag, Favorite, Visit, BusinessOwnerProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'color', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'category']
    list_filter = ['category']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'owner', 'created_by_owner', 'status', 'neighborhood', 'rating', 'review_count', 'verified', 'is_active']
    list_filter = ['category', 'status', 'created_by_owner', 'neighborhood', 'verified', 'is_active', 'is_featured']
    search_fields = ['name', 'description', 'address']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['features', 'tags']
    readonly_fields = ['rating', 'review_count', 'views', 'favorites_count', 'visits_count', 'created_at', 'updated_at']
    
    actions = ['approve_businesses', 'reject_businesses', 'mark_as_pending']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'description', 'short_description', 'category', 'subcategory', 'tags')
        }),
        ('Control de Propietario', {
            'fields': ('owner', 'created_by_owner', 'status', 'approved_by', 'approved_at', 'rejection_reason')
        }),
        ('Ubicación', {
            'fields': ('latitude', 'longitude', 'address', 'neighborhood', 'comuna')
        }),
        ('Contacto', {
            'fields': ('phone', 'email', 'website', 'instagram')
        }),
        ('Horarios y Características', {
            'fields': ('hours', 'is_open_24h', 'features', 'price_range')
        }),
        ('Media', {
            'fields': ('cover_image', 'logo', 'images')
        }),
        ('Ratings y Verificación', {
            'fields': ('rating', 'review_count', 'verified', 'claimed')
        }),
        ('Estadísticas', {
            'fields': ('views', 'favorites_count', 'visits_count')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_featured', 'created_at', 'updated_at')
        }),
    )
    
    def approve_businesses(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(
            status='published',
            verified=True,
            approved_by=request.user,
            approved_at=timezone.now()
        )
        self.message_user(request, f"{updated} negocios aprobados y publicados")
    approve_businesses.short_description = "✅ Aprobar y publicar negocios"
    
    def reject_businesses(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} negocios rechazados")
    reject_businesses.short_description = "❌ Rechazar negocios"
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending_review')
        self.message_user(request, f"{updated} negocios marcados como pendientes")
    mark_as_pending.short_description = "⏳ Marcar como pendiente de revisión"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'business', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'business__name']
    date_hierarchy = 'created_at'


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['user', 'business', 'route', 'visited_at']
    list_filter = ['visited_at']
    search_fields = ['user__email', 'business__name']
    date_hierarchy = 'visited_at'


@admin.register(BusinessOwnerProfile)
class BusinessOwnerProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user_email',
        'can_create_businesses',
        'max_businesses_allowed',
        'businesses_created_count',
        'remaining_slots',
        'is_verified_owner'
    ]
    list_filter = ['can_create_businesses', 'is_verified_owner']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['businesses_created_count', 'remaining_slots', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Permisos', {
            'fields': ('can_create_businesses', 'max_businesses_allowed', 'is_verified_owner')
        }),
        ('Estadísticas', {
            'fields': ('businesses_created_count', 'remaining_slots')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['grant_1_business', 'grant_3_businesses', 'grant_unlimited', 'revoke_permissions']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    
    def grant_1_business(self, request, queryset):
        queryset.update(can_create_businesses=True, max_businesses_allowed=1)
        self.message_user(request, f"{queryset.count()} usuarios pueden crear 1 negocio")
    grant_1_business.short_description = "Permitir crear 1 negocio"
    
    def grant_3_businesses(self, request, queryset):
        queryset.update(can_create_businesses=True, max_businesses_allowed=3)
        self.message_user(request, f"{queryset.count()} usuarios pueden crear 3 negocios")
    grant_3_businesses.short_description = "Permitir crear 3 negocios"
    
    def grant_unlimited(self, request, queryset):
        queryset.update(can_create_businesses=True, max_businesses_allowed=-1)
        self.message_user(request, f"{queryset.count()} usuarios pueden crear negocios ilimitados")
    grant_unlimited.short_description = "Permitir crear ilimitados"
    
    def revoke_permissions(self, request, queryset):
        queryset.update(can_create_businesses=False, max_businesses_allowed=0)
        self.message_user(request, f"{queryset.count()} permisos revocados")
    revoke_permissions.short_description = "Revocar permisos"
