from django.contrib import admin
from .models import Business, Category, Feature, Tag, Favorite, Visit


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
    list_display = ['name', 'category', 'neighborhood', 'rating', 'review_count', 'verified', 'is_active']
    list_filter = ['category', 'neighborhood', 'verified', 'is_active', 'is_featured']
    search_fields = ['name', 'description', 'address']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['features', 'tags']
    readonly_fields = ['rating', 'review_count', 'views', 'favorites_count', 'visits_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'description', 'short_description', 'category', 'subcategory', 'tags')
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
            'fields': ('rating', 'review_count', 'verified', 'claimed', 'owner')
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
