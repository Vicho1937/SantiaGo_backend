from django.contrib import admin
from .models import Review, ReviewHelpful


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'business', 'rating', 'would_recommend', 'is_approved', 'is_verified_visit', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_verified_visit', 'would_recommend', 'created_at']
    search_fields = ['user__email', 'business__name', 'title', 'comment']
    readonly_fields = ['helpful_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Usuario y Negocio', {
            'fields': ('user', 'business')
        }),
        ('Review', {
            'fields': ('rating', 'title', 'comment', 'would_recommend', 'images')
        }),
        ('Estado', {
            'fields': ('is_approved', 'is_verified_visit', 'helpful_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ReviewHelpful)
class ReviewHelpfulAdmin(admin.ModelAdmin):
    list_display = ['review', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'review__business__name']
    date_hierarchy = 'created_at'
