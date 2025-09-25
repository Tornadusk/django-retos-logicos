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
    foto_perfil = models.ImageField(
        upload_to='perfiles/', 
        blank=True, 
        null=True,
        help_text="Sube una foto personalizada o deja vacío para usar avatar por defecto"
    )
    avatar_por_defecto = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[
            ('👨', '👨 Hombre'),
            ('👩', '👩 Mujer'),
            ('👨‍💼', '👨‍💼 Profesional'),
            ('👩‍💼', '👩‍💼 Profesional'),
            ('👨‍🎓', '👨‍🎓 Estudiante'),
            ('👩‍🎓', '👩‍🎓 Estudiante'),
            ('👨‍💻', '👨‍💻 Desarrollador'),
            ('👩‍💻', '👩‍💻 Desarrolladora'),
        ],
        help_text="Selecciona un avatar por defecto si no tienes foto personal"
    )
    
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
    
    def obtener_avatar(self):
        """Retorna la foto de perfil si existe, o el avatar por defecto"""
        if self.foto_perfil:
            return self.foto_perfil.url
        return self.avatar_por_defecto or '👤'
    
    def tiene_foto_personal(self):
        """Verifica si el usuario tiene una foto personal subida"""
        return bool(self.foto_perfil)
    
    def eliminar_foto_personal(self):
        """Elimina la foto personal del usuario"""
        if self.foto_perfil:
            self.foto_perfil.delete(save=False)
            self.foto_perfil = None
            self.save()

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea automáticamente un perfil cuando se crea un usuario"""
    if created:
        # Verificar si ya existe un perfil para evitar duplicados
        if not hasattr(instance, 'perfil'):
            PerfilUsuario.objects.create(usuario=instance)
