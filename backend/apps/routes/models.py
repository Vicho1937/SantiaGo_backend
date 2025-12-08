import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.businesses.models import Business

User = get_user_model()


class Route(models.Model):
    """Rutas creadas por usuarios"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routes')
    
    # Info básica
    name = models.CharField(max_length=255, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    
    # Configuración
    is_public = models.BooleanField(default=False, verbose_name="Pública")
    is_featured = models.BooleanField(default=False, verbose_name="Destacada")
    
    # Stats calculados
    total_distance = models.FloatField(default=0, help_text="Distancia en km")
    estimated_duration = models.IntegerField(default=0, help_text="Duración en minutos")
    stops_count = models.IntegerField(default=0, verbose_name="Número de paradas")
    
    # Engagement
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'routes'
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.email}"
    
    def update_stats(self):
        """Actualizar estadísticas de la ruta"""
        stops = self.stops.all().order_by('order')
        self.stops_count = stops.count()
        
        # Calcular duración total
        total_duration = sum(stop.duration for stop in stops)
        self.estimated_duration = total_duration
        
        # Calcular distancia total (simplificado)
        # TODO: Usar Mapbox API para distancias reales
        self.total_distance = 0
        
        self.save(update_fields=['stops_count', 'estimated_duration', 'total_distance'])


class RouteStop(models.Model):
    """Paradas individuales en una ruta"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='route_stops')
    
    # Orden en la ruta
    order = models.IntegerField(verbose_name="Orden")
    
    # Tiempos estimados
    duration = models.IntegerField(default=60, help_text="Tiempo en el lugar (minutos)")
    notes = models.TextField(blank=True, verbose_name="Notas")
    
    # Completado
    is_completed = models.BooleanField(default=False, verbose_name="Completada")
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'route_stops'
        ordering = ['order']
        unique_together = ['route', 'order']
        verbose_name = 'Parada de Ruta'
        verbose_name_plural = 'Paradas de Ruta'
    
    def __str__(self):
        return f"{self.route.name} - Stop {self.order}: {self.business.name}"


class RouteLike(models.Model):
    """Likes en rutas"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='liked_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_routes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'route_likes'
        unique_together = ['route', 'user']
    
    def __str__(self):
        return f"{self.user.email} - {self.route.name}"
