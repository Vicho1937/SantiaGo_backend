from django.contrib import admin
from .models import Route, RouteStop, RouteLike


class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 0
    readonly_fields = ['is_completed', 'completed_at']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'stops_count', 'is_public', 'is_featured', 'likes', 'views', 'created_at']
    list_filter = ['is_public', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'user__email']
    readonly_fields = ['stops_count', 'total_distance', 'estimated_duration', 'views', 'likes', 'shares', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    inlines = [RouteStopInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('user', 'name', 'description')
        }),
        ('Configuración', {
            'fields': ('is_public', 'is_featured')
        }),
        ('Estadísticas', {
            'fields': ('stops_count', 'total_distance', 'estimated_duration', 'views', 'likes', 'shares')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ['route', 'business', 'order', 'duration', 'is_completed']
    list_filter = ['is_completed']
    search_fields = ['route__name', 'business__name']


@admin.register(RouteLike)
class RouteLikeAdmin(admin.ModelAdmin):
    list_display = ['route', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['route__name', 'user__email']
    date_hierarchy = 'created_at'
