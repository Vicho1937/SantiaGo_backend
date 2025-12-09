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
