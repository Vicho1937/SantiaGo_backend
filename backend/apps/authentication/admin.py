from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin personalizado para gestión de usuarios"""
    
    list_display = [
        'email', 'username', 'full_name', 'is_active', 'is_staff', 
        'is_superuser', 'has_owner_profile', 'routes_created', 
        'businesses_visited', 'date_joined_formatted'
    ]
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 
        'notifications_enabled', 'profile_visibility',
        'theme_preference', 'created_at'
    ]
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    readonly_fields = [
        'id', 'google_id', 'github_id', 'routes_created', 
        'businesses_visited', 'created_at', 'updated_at', 'last_login_at'
    ]
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('id', 'email', 'username', 'password')
        }),
        ('Datos Personales', {
            'fields': ('first_name', 'last_name', 'phone', 'avatar', 'avatar_thumbnail', 'bio')
        }),
        ('OAuth', {
            'fields': ('google_id', 'github_id'),
            'classes': ('collapse',)
        }),
        ('Ubicación', {
            'fields': ('location_city', 'location_state', 'location_country')
        }),
        ('Preferencias', {
            'fields': ('preferred_language', 'notifications_enabled', 'theme_preference')
        }),
        ('Privacidad', {
            'fields': ('profile_visibility', 'show_email', 'show_phone', 'show_location', 'show_activity')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Estadísticas', {
            'fields': ('routes_created', 'businesses_visited')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'last_login_at', 'last_login')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    
    filter_horizontal = ('groups', 'user_permissions')
    
    actions = [
        'activate_users', 'deactivate_users', 
        'make_staff', 'remove_staff',
        'enable_notifications', 'disable_notifications'
    ]
    
    def full_name(self, obj):
        name = f"{obj.first_name} {obj.last_name}".strip()
        return name if name else '-'
    full_name.short_description = 'Nombre Completo'
    
    def date_joined_formatted(self, obj):
        return obj.created_at.strftime('%d/%m/%Y %H:%M') if obj.created_at else '-'
    date_joined_formatted.short_description = 'Fecha Registro'
    
    def has_owner_profile(self, obj):
        return hasattr(obj, 'owner_profile')
    has_owner_profile.boolean = True
    has_owner_profile.short_description = 'Es Propietario'
    
    # Acciones masivas
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"✅ {updated} usuarios activados")
    activate_users.short_description = "✅ Activar usuarios seleccionados"
    
    def deactivate_users(self, request, queryset):
        # No desactivar superusuarios
        updated = queryset.filter(is_superuser=False).update(is_active=False)
        self.message_user(request, f"❌ {updated} usuarios desactivados")
    deactivate_users.short_description = "❌ Desactivar usuarios seleccionados"
    
    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f"👔 {updated} usuarios ahora son staff")
    make_staff.short_description = "👔 Convertir en staff"
    
    def remove_staff(self, request, queryset):
        updated = queryset.filter(is_superuser=False).update(is_staff=False)
        self.message_user(request, f"👤 {updated} usuarios ya no son staff")
    remove_staff.short_description = "👤 Quitar rol de staff"
    
    def enable_notifications(self, request, queryset):
        updated = queryset.update(notifications_enabled=True)
        self.message_user(request, f"🔔 Notificaciones activadas para {updated} usuarios")
    enable_notifications.short_description = "🔔 Activar notificaciones"
    
    def disable_notifications(self, request, queryset):
        updated = queryset.update(notifications_enabled=False)
        self.message_user(request, f"🔕 Notificaciones desactivadas para {updated} usuarios")
    disable_notifications.short_description = "🔕 Desactivar notificaciones"
