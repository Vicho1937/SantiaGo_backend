import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Usuario extendido con campos personalizados"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.URLField(blank=True)
    avatar_thumbnail = models.URLField(blank=True)
    bio = models.TextField(blank=True, max_length=500)

    # OAuth providers
    google_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
    github_id = models.CharField(max_length=255, blank=True, unique=True, null=True)

    # Ubicación
    location_city = models.CharField(max_length=100, blank=True)
    location_state = models.CharField(max_length=100, blank=True)
    location_country = models.CharField(max_length=100, blank=True, default='Chile')

    # Preferencias
    preferred_language = models.CharField(max_length=10, default='es')
    notifications_enabled = models.BooleanField(default=True)
    theme_preference = models.CharField(max_length=10, default='auto', choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ])

    # Privacidad
    profile_visibility = models.CharField(max_length=10, default='public', choices=[
        ('public', 'Public'),
        ('friends', 'Friends'),
        ('private', 'Private'),
    ])
    show_email = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=False)
    show_location = models.BooleanField(default=False)
    show_activity = models.BooleanField(default=True)

    # Stats
    routes_created = models.IntegerField(default=0)
    businesses_visited = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.email
