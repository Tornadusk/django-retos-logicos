"""
APP "cuentas" - GESTIÓN DE USUARIOS
===================================

Esta app se encarga de:
- Gestión de usuarios: registro, login, perfiles
- Autenticación y autorización
- Perfiles extendidos de usuario
- Información personal y estadísticas básicas

Modelos principales:
- PerfilUsuario: Información extendida del usuario (puntuación, nivel, etc.)

Trabaja en conjunto con las apps "retos" y "juego" para proporcionar
la base de usuarios del sistema.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    """Modelo de usuario personalizado basado en AbstractUser.
    Espacio para futuros campos adicionales.
    """
    pass

class PerfilUsuario(models.Model):
    """Perfil extendido del usuario para el sistema de retos"""
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    puntuacion_total = models.IntegerField(default=0)
    nivel = models.IntegerField(default=1)
    retos_completados = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        ordering = ['-puntuacion_total']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.puntuacion_total} pts"
    
    def actualizar_puntuacion(self):
        """Actualiza la puntuación total basada en los intentos correctos"""
        from juego.models import Intento
        puntuacion = Intento.objects.filter(
            usuario=self.usuario,
            es_correcto=True
        ).aggregate(total=models.Sum('puntuacion_obtenida'))['total'] or 0
        self.puntuacion_total = puntuacion
        self.retos_completados = Intento.objects.filter(
            usuario=self.usuario,
            es_correcto=True
        ).values('reto').distinct().count()
        self.save()

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea automáticamente un perfil cuando se crea un usuario"""
    if created:
        # Verificar si ya existe un perfil para evitar duplicados
        if not hasattr(instance, 'perfil'):
            PerfilUsuario.objects.create(usuario=instance)
