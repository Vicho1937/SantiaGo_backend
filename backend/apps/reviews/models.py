import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.businesses.models import Business

User = get_user_model()


class Review(models.Model):
    """Reseñas de negocios"""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reviews')
    
    # Rating
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Calificación")
    
    # Contenido
    title = models.CharField(max_length=200, blank=True, verbose_name="Título")
    comment = models.TextField(verbose_name="Comentario")
    
    # Recomendación
    would_recommend = models.BooleanField(default=True, verbose_name="Recomendaría")
    
    # Fotos
    images = models.JSONField(default=list, blank=True, help_text="URLs de imágenes")
    
    # Engagement
    helpful_count = models.IntegerField(default=0, verbose_name="Útil")
    
    # Status
    is_verified_visit = models.BooleanField(default=False, verbose_name="Visita verificada")
    is_approved = models.BooleanField(default=True, verbose_name="Aprobada")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reviews'
        unique_together = ['user', 'business']
        ordering = ['-created_at']
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
    
    def __str__(self):
        return f"{self.user.email} - {self.business.name} ({self.rating}⭐)"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar rating del negocio
        self.business.update_rating()


class ReviewHelpful(models.Model):
    """Registro de usuarios que marcaron una review como útil"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='helpful_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'review_helpful'
        unique_together = ['review', 'user']
    
    def __str__(self):
        return f"{self.user.email} - {self.review.id}"
