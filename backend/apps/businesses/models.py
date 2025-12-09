import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    """Categorías de negocios"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text="Nombre del icono Lucide")
    color = models.CharField(max_length=7, default='#000000', help_text="Color en formato hex")
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tags para negocios"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        db_table = 'tags'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Feature(models.Model):
    """Características de los negocios"""
    CATEGORY_CHOICES = [
        ('amenity', 'Amenidad'),
        ('accessibility', 'Accesibilidad'),
        ('payment', 'Métodos de Pago'),
        ('service', 'Servicio'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text="Nombre del icono")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='amenity')
    
    class Meta:
        db_table = 'features'
        verbose_name = 'Característica'
        verbose_name_plural = 'Características'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Business(models.Model):
    """Negocios locales de Santiago"""
    PRICE_RANGE_CHOICES = [
        (1, '$'),
        (2, '$$'),
        (3, '$$$'),
        (4, '$$$$'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Info básica
    name = models.CharField(max_length=255, verbose_name="Nombre")
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name="Descripción")
    short_description = models.CharField(max_length=200, verbose_name="Descripción corta")
    
    # Categorización
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='businesses')
    subcategory = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='businesses')
    
    # Contacto y ubicación
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    
    # Geolocalización (sin PostGIS por ahora - usar lat/lng simples)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Latitud")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Longitud")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    neighborhood = models.CharField(max_length=100, verbose_name="Barrio")
    comuna = models.CharField(max_length=100, verbose_name="Comuna")
    
    # Horarios (JSON format)
    hours = models.JSONField(default=dict, blank=True, help_text="Horarios de atención")
    is_open_24h = models.BooleanField(default=False, verbose_name="Abierto 24h")
    
    # Características
    features = models.ManyToManyField(Feature, blank=True, related_name='businesses')
    price_range = models.IntegerField(choices=PRICE_RANGE_CHOICES, default=2, verbose_name="Rango de precio")
    
    # Media
    images = models.JSONField(default=list, blank=True, help_text="URLs de imágenes")
    cover_image = models.URLField(verbose_name="Imagen de portada")
    logo = models.URLField(blank=True)
    
    # Ratings y verificación
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Rating")
    review_count = models.IntegerField(default=0, verbose_name="Cantidad de reseñas")
    verified = models.BooleanField(default=False, verbose_name="Verificado")
    claimed = models.BooleanField(default=False, verbose_name="Reclamado")
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='owned_businesses')
    
    # Control de creación y aprobación
    created_by_owner = models.BooleanField(default=False, verbose_name="Creado por propietario")
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Borrador'),
            ('pending_review', 'Pendiente de Revisión'),
            ('published', 'Publicado'),
            ('rejected', 'Rechazado'),
        ],
        default='published',
        verbose_name="Estado"
    )
    approved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_businesses',
        verbose_name="Aprobado por"
    )
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de aprobación")
    rejection_reason = models.TextField(blank=True, verbose_name="Razón de rechazo")
    
    # Stats
    views = models.IntegerField(default=0)
    favorites_count = models.IntegerField(default=0)
    visits_count = models.IntegerField(default=0)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, verbose_name="Destacado")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'businesses'
        verbose_name = 'Negocio'
        verbose_name_plural = 'Negocios'
        ordering = ['-rating', '-review_count']
        indexes = [
            models.Index(fields=['category', 'neighborhood']),
            models.Index(fields=['rating', '-created_at']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def update_rating(self):
        """Actualizar rating promedio basado en reviews"""
        from apps.reviews.models import Review
        reviews = Review.objects.filter(business=self, is_approved=True)
        if reviews.exists():
            from django.db.models import Avg
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            self.rating = round(avg_rating, 2)
            self.review_count = reviews.count()
            self.save(update_fields=['rating', 'review_count'])


class Favorite(models.Model):
    """Negocios favoritos de usuarios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'favorites'
        unique_together = ['user', 'business']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.business.name}"


class Visit(models.Model):
    """Registro de visitas a negocios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='visits')
    route = models.ForeignKey('routes.Route', null=True, blank=True, on_delete=models.SET_NULL)
    visited_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'visits'
        ordering = ['-visited_at']
    
    def __str__(self):
        return f"{self.user.email} visitó {self.business.name}"
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BusinessOwnerProfile(models.Model):
    """Perfil de propietario de negocio"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    
    # Permisos
    can_create_businesses = models.BooleanField(default=False, verbose_name="Puede crear negocios")
    max_businesses_allowed = models.IntegerField(
        default=0,
        verbose_name="Máximo de negocios permitidos",
        help_text="-1 para ilimitado, 0 para ninguno"
    )
    
    # Verificación
    is_verified_owner = models.BooleanField(default=False, verbose_name="Propietario verificado")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'business_owner_profiles'
        verbose_name = 'Perfil de Propietario'
        verbose_name_plural = 'Perfiles de Propietarios'
    
    def __str__(self):
        return f"{self.user.email} - {'Activo' if self.can_create_businesses else 'Inactivo'}"
    
    @property
    def businesses_created_count(self):
        return self.user.owned_businesses.filter(created_by_owner=True).count()
    
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
