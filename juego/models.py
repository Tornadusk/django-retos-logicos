"""
APP "juego" - EXPERIENCIA DEL USUARIO
====================================

Esta app se encarga de:
- Interacciones del usuario: intentos, respuestas, puntuaciones
- Sistema de ranking: clasificación de usuarios
- Progreso personal: qué ha resuelto cada usuario
- Estadísticas de usuario: perfil, nivel, retos completados
- Lógica de puntuación: cuántos puntos gana por cada reto

Modelos principales:
- Intento: Cada vez que un usuario intenta resolver un reto
- Ranking: Clasificación global de usuarios
- PerfilUsuario: Información extendida del usuario

Trabaja en conjunto con la app "retos" que maneja el contenido educativo.

FLUJO DE TRABAJO:
retos (contenido) ←→ juego (interacción)
     ↓                    ↓
   "El problema"      "Usuario intenta"
   "Respuesta: 17"    "Escribe: 17 minutos"
   "Puntos: 40"       "Gana: 40 puntos"
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from retos.models import Reto
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Intento(models.Model):
    """Modelo para registrar los intentos de los usuarios en los retos"""
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='intentos')
    reto = models.ForeignKey(Reto, on_delete=models.CASCADE, related_name='intentos')
    respuesta_usuario = models.TextField()
    es_correcto = models.BooleanField(default=False)
    puntuacion_obtenida = models.IntegerField(default=0)
    fecha_intento = models.DateTimeField(auto_now_add=True)
    tiempo_respuesta = models.DurationField(null=True, blank=True, help_text="Tiempo que tardó en responder")
    
    class Meta:
        verbose_name = "Intento"
        verbose_name_plural = "Intentos"
        ordering = ['-fecha_intento']
    
    def __str__(self):
        estado = "✓" if self.es_correcto else "✗"
        return f"{self.usuario.username} - {self.reto.titulo} {estado}"
    
    def calcular_puntuacion(self):
        """Calcula la puntuación basada en la dificultad y tiempo de respuesta"""
        if not self.es_correcto:
            return 0
        
        # Verificar si ya había resuelto correctamente este reto antes
        # Solo verificar si ya tenemos un ID (objeto ya guardado)
        if self.pk:
            intentos_anteriores_correctos = Intento.objects.filter(
                usuario=self.usuario,
                reto=self.reto,
                es_correcto=True
            ).exclude(pk=self.pk).exists()
            
            # Solo otorgar puntos si es el primer intento correcto
            if intentos_anteriores_correctos:
                return 0
        
        # Puntuación base según dificultad
        puntuacion_base = self.reto.puntos
        
        # Bonificación por tiempo (si se registró)
        if self.tiempo_respuesta:
            # Bonificación del 20% si responde en menos de 5 minutos
            if self.tiempo_respuesta.total_seconds() < 300:  # 5 minutos
                puntuacion_base = int(puntuacion_base * 1.2)
        
        return puntuacion_base
    
    def save(self, *args, **kwargs):
        """Override save para calcular automáticamente la puntuación"""
        if self.es_correcto:
            self.puntuacion_obtenida = self.calcular_puntuacion()
        super().save(*args, **kwargs)
        
        # Actualizar estadísticas del reto
        self.reto.actualizar_estadisticas()
        
        # Actualizar perfil del usuario
        if hasattr(self.usuario, 'perfil'):
            self.usuario.perfil.actualizar_puntuacion()

class Ranking(models.Model):
    """Modelo para el ranking de usuarios"""
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ranking')
    posicion = models.IntegerField()
    puntuacion_total = models.IntegerField(default=0)
    retos_completados = models.IntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Ranking"
        verbose_name_plural = "Rankings"
        ordering = ['posicion']
    
    def __str__(self):
        return f"#{self.posicion} {self.usuario.username} - {self.puntuacion_total} pts"
    
    @classmethod
    def actualizar_ranking(cls):
        """Actualiza el ranking de todos los usuarios"""
        from cuentas.models import PerfilUsuario
        
        # Obtener usuarios ordenados por puntuación
        perfiles = PerfilUsuario.objects.all().order_by('-puntuacion_total')
        
        # Actualizar o crear entradas de ranking
        for posicion, perfil in enumerate(perfiles, 1):
            ranking, created = cls.objects.get_or_create(
                usuario=perfil.usuario,
                defaults={
                    'posicion': posicion,
                    'puntuacion_total': perfil.puntuacion_total,
                    'retos_completados': perfil.retos_completados,
                }
            )
            if not created:
                ranking.posicion = posicion
                ranking.puntuacion_total = perfil.puntuacion_total
                ranking.retos_completados = perfil.retos_completados
                ranking.save()


# Si se borra un intento individual, actualizar el perfil del usuario y el ranking
@receiver(post_delete, sender=Intento)
def intento_post_delete_update_profile(sender, instance: Intento, **kwargs):
    try:
        if hasattr(instance.usuario, 'perfil'):
            instance.usuario.perfil.actualizar_puntuacion()
        Ranking.actualizar_ranking()
    except Exception:
        pass
