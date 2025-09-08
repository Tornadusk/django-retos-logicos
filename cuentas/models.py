from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    """Perfil extendido del usuario para el sistema de retos"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
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
        PerfilUsuario.objects.create(usuario=instance)
