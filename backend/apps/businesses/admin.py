from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import (
    Business, Category, Feature, Tag, Favorite, Visit, 
    BusinessOwnerProfile, BusinessView, BusinessImage, OpeningHours, Report
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'color_preview', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    def color_preview(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 5px 15px; border-radius: 3px;">{}</span>',
            obj.color, obj.color
        )
    color_preview.short_description = 'Color'


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


class BusinessImageInline(admin.TabularInline):
    """Inline para imágenes del negocio"""
    model = BusinessImage
    extra = 1
    fields = ['image_url', 'image_type', 'caption', 'order', 'is_active', 'is_approved']
    readonly_fields = []


class OpeningHoursInline(admin.TabularInline):
    """Inline para horarios del negocio"""
    model = OpeningHours
    extra = 0
    fields = ['day_of_week', 'opens_at', 'closes_at', 'opens_at_2', 'closes_at_2', 'is_closed', 'is_24h', 'notes']


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'owner', 'owner_has_permissions', 'created_by_owner', 'status', 'neighborhood', 'rating', 'review_count', 'verified', 'is_active']
    list_filter = ['category', 'status', 'created_by_owner', 'neighborhood', 'verified', 'is_active', 'is_featured']
    search_fields = ['name', 'description', 'address', 'owner__email']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['features', 'tags']
    readonly_fields = ['rating', 'review_count', 'views', 'favorites_count', 'visits_count', 'created_at', 'updated_at']
    inlines = [BusinessImageInline, OpeningHoursInline]

    actions = ['approve_businesses', 'reject_businesses', 'mark_as_pending', 'auto_publish_approved_owners']

    def owner_has_permissions(self, obj):
        """Indica si el propietario tiene permisos aprobados"""
        if obj.owner and obj.created_by_owner:
            try:
                profile = BusinessOwnerProfile.objects.get(user=obj.owner)
                return profile.can_create_businesses
            except BusinessOwnerProfile.DoesNotExist:
                return False
        return None
    owner_has_permissions.boolean = True
    owner_has_permissions.short_description = 'Propietario Aprobado'
    
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

    def auto_publish_approved_owners(self, request, queryset):
        """
        Publica automáticamente negocios que están pendientes pero pertenecen
        a usuarios con permisos aprobados (can_create_businesses=True)
        """
        # Filtrar solo negocios pendientes creados por propietarios
        pending_businesses = queryset.filter(
            status='pending_review',
            created_by_owner=True
        )

        # Obtener IDs de usuarios con permisos
        approved_profiles = BusinessOwnerProfile.objects.filter(can_create_businesses=True)
        approved_user_ids = approved_profiles.values_list('user_id', flat=True)

        # Filtrar negocios de usuarios aprobados
        businesses_to_publish = pending_businesses.filter(owner_id__in=approved_user_ids)

        updated = businesses_to_publish.update(
            status='published',
            approved_by=request.user,
            approved_at=timezone.now()
        )

        if updated > 0:
            self.message_user(
                request,
                f"✅ {updated} negocios publicados automáticamente (propietarios con permisos aprobados)",
                level='success'
            )
        else:
            self.message_user(
                request,
                "No se encontraron negocios pendientes de propietarios aprobados en la selección",
                level='warning'
            )

    auto_publish_approved_owners.short_description = "🚀 Auto-publicar negocios de propietarios aprobados"


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


@admin.register(BusinessView)
class BusinessViewAdmin(admin.ModelAdmin):
    """Admin para vistas de negocios (analytics)"""
    list_display = ['business', 'viewed_at', 'ip_address', 'session_key_short']
    list_filter = ['viewed_at', 'business__category']
    search_fields = ['business__name', 'ip_address']
    date_hierarchy = 'viewed_at'
    readonly_fields = ['business', 'viewed_at', 'session_key', 'ip_address', 'user_agent']
    
    def session_key_short(self, obj):
        if obj.session_key:
            return obj.session_key[:10] + '...'
        return '-'
    session_key_short.short_description = 'Sesión'
    
    def has_add_permission(self, request):
        return False  # No permitir crear manualmente


@admin.register(BusinessImage)
class BusinessImageAdmin(admin.ModelAdmin):
    """Admin para imágenes de negocios"""
    list_display = ['business', 'image_type', 'thumbnail_preview', 'caption', 'order', 'is_active', 'is_approved', 'uploaded_by', 'created_at']
    list_filter = ['image_type', 'is_active', 'is_approved', 'created_at']
    search_fields = ['business__name', 'caption', 'alt_text']
    date_hierarchy = 'created_at'
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Negocio', {
            'fields': ('business',)
        }),
        ('Imagen', {
            'fields': ('image_url', 'thumbnail_url', 'image_type')
        }),
        ('Metadatos', {
            'fields': ('caption', 'alt_text', 'order')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_approved', 'uploaded_by')
        }),
        ('Info', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_images', 'reject_images', 'set_as_cover']
    
    def thumbnail_preview(self, obj):
        url = obj.thumbnail_url or obj.image_url
        if url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px; object-fit: cover;" />', url)
        return '-'
    thumbnail_preview.short_description = 'Preview'
    
    def approve_images(self, request, queryset):
        updated = queryset.update(is_approved=True, is_active=True)
        self.message_user(request, f"✅ {updated} imágenes aprobadas")
    approve_images.short_description = "✅ Aprobar imágenes"
    
    def reject_images(self, request, queryset):
        updated = queryset.update(is_approved=False, is_active=False)
        self.message_user(request, f"❌ {updated} imágenes rechazadas")
    reject_images.short_description = "❌ Rechazar imágenes"
    
    def set_as_cover(self, request, queryset):
        for img in queryset:
            img.image_type = 'cover'
            img.order = 0
            img.save()
        self.message_user(request, f"🖼️ {queryset.count()} imágenes marcadas como portada")
    set_as_cover.short_description = "🖼️ Establecer como portada"


@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    """Admin para horarios de apertura"""
    list_display = ['business', 'day_display', 'hours_display', 'is_closed', 'is_24h']
    list_filter = ['day_of_week', 'is_closed', 'is_24h']
    search_fields = ['business__name']
    ordering = ['business', 'day_of_week']
    
    fieldsets = (
        ('Negocio y Día', {
            'fields': ('business', 'day_of_week')
        }),
        ('Horario Principal', {
            'fields': ('opens_at', 'closes_at')
        }),
        ('Segundo Turno (opcional)', {
            'fields': ('opens_at_2', 'closes_at_2'),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('is_closed', 'is_24h', 'notes')
        }),
    )
    
    def day_display(self, obj):
        return obj.get_day_of_week_display()
    day_display.short_description = 'Día'
    
    def hours_display(self, obj):
        if obj.is_closed:
            return format_html('<span style="color: red;">Cerrado</span>')
        if obj.is_24h:
            return format_html('<span style="color: green;">24 horas</span>')
        hours = f"{obj.opens_at.strftime('%H:%M') if obj.opens_at else '-'} - {obj.closes_at.strftime('%H:%M') if obj.closes_at else '-'}"
        if obj.opens_at_2 and obj.closes_at_2:
            hours += f" / {obj.opens_at_2.strftime('%H:%M')} - {obj.closes_at_2.strftime('%H:%M')}"
        return hours
    hours_display.short_description = 'Horario'


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin para gestión de reportes de contenido inapropiado"""
    list_display = [
        'id_short', 'content_type', 'reason', 'status_badge', 
        'reporter', 'reported_content', 'created_at', 'reviewed_by'
    ]
    list_filter = ['status', 'content_type', 'reason', 'action_taken', 'created_at']
    search_fields = ['reporter__email', 'description', 'business__name', 'reported_user__email']
    date_hierarchy = 'created_at'
    readonly_fields = ['id', 'reporter', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Reporte', {
            'fields': ('id', 'reporter', 'content_type', 'reason', 'description', 'evidence_urls')
        }),
        ('Contenido Reportado', {
            'fields': ('business', 'review', 'image', 'reported_user'),
            'description': 'Solo uno de estos campos debe estar lleno según el tipo de contenido'
        }),
        ('Estado', {
            'fields': ('status',)
        }),
        ('Resolución', {
            'fields': ('action_taken', 'resolution_notes', 'reviewed_by', 'reviewed_at')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_reviewing', 'resolve_no_action', 'resolve_content_removed', 'dismiss_report']
    
    def id_short(self, obj):
        return str(obj.id)[:8]
    id_short.short_description = 'ID'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FFA500',      # Naranja
            'reviewing': '#1E90FF',    # Azul
            'resolved': '#32CD32',     # Verde
            'dismissed': '#808080',    # Gris
        }
        color = colors.get(obj.status, '#000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Estado'
    
    def reported_content(self, obj):
        if obj.business:
            return f"Negocio: {obj.business.name}"
        if obj.review:
            return f"Reseña de: {obj.review.user.email}"
        if obj.image:
            return f"Imagen: {obj.image.business.name}"
        if obj.reported_user:
            return f"Usuario: {obj.reported_user.email}"
        return '-'
    reported_content.short_description = 'Contenido'
    
    def mark_reviewing(self, request, queryset):
        queryset.filter(status='pending').update(
            status='reviewing',
            reviewed_by=request.user
        )
        self.message_user(request, f"🔍 {queryset.count()} reportes en revisión")
    mark_reviewing.short_description = "🔍 Marcar en revisión"
    
    def resolve_no_action(self, request, queryset):
        queryset.update(
            status='resolved',
            action_taken='no_action',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f"✅ {queryset.count()} reportes resueltos sin acción")
    resolve_no_action.short_description = "✅ Resolver - Sin acción necesaria"
    
    def resolve_content_removed(self, request, queryset):
        queryset.update(
            status='resolved',
            action_taken='content_removed',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f"🗑️ {queryset.count()} reportes resueltos - contenido eliminado")
    resolve_content_removed.short_description = "🗑️ Resolver - Contenido eliminado"
    
    def dismiss_report(self, request, queryset):
        queryset.update(
            status='dismissed',
            action_taken='no_action',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f"❌ {queryset.count()} reportes desestimados")
    dismiss_report.short_description = "❌ Desestimar reporte"
