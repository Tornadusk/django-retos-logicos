from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from retos.models import Reto

class Intento(models.Model):
    """Modelo para registrar los intentos de los usuarios en los retos"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='intentos')
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
        unique_together = ['usuario', 'reto']  # Un usuario solo puede intentar un reto una vez
    
    def __str__(self):
        estado = "✓" if self.es_correcto else "✗"
        return f"{self.usuario.username} - {self.reto.titulo} {estado}"
    
    def calcular_puntuacion(self):
        """Calcula la puntuación basada en la dificultad y tiempo de respuesta"""
        if not self.es_correcto:
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
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ranking')
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
