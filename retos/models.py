"""
APP "retos" - GESTIÓN DE CONTENIDO EDUCATIVO
============================================

Esta app se encarga de:
- Crear y gestionar los retos (problemas, puzzles, desafíos)
- Contenido educativo: enunciados, respuestas correctas, explicaciones
- Clasificación: categorías, dificultad, puntos
- Configuración: número máximo de intentos, orden de prioridad
- Respuestas alternativas: múltiples formatos de la misma respuesta
- Estadísticas básicas: intentos totales, intentos exitosos

Modelos principales:
- Reto: El problema/puzzle en sí
- Categoria: Clasificación de los retos
- RespuestaAlternativa: Variaciones de respuestas correctas
- ConfiguracionOrdenamiento: Cómo mostrar los retos

Trabaja en conjunto con la app "juego" que maneja la interacción del usuario.
"""

from django.db import models
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import re

class Categoria(models.Model):
    """Categorías para clasificar los retos"""
    DIFICULTAD_CHOICES = [
        ('facil', 'Fácil'),
        ('medio', 'Medio'),
        ('dificil', 'Difícil'),
        ('experto', 'Experto'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Color en formato hexadecimal")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Reto(models.Model):
    """Modelo para los retos lógicos matemáticos"""
    DIFICULTAD_CHOICES = [
        ('facil', 'Fácil'),
        ('medio', 'Medio'),
        ('dificil', 'Difícil'),
        ('experto', 'Experto'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(help_text="Descripción breve del reto")
    enunciado = models.TextField(help_text="Enunciado completo del problema")
    respuesta_correcta = models.TextField(help_text="Respuesta correcta")
    explicacion = models.TextField(blank=True, help_text="Explicación de la solución")
    ejemplo_entrada = models.TextField(blank=True, help_text="Ejemplo de cómo escribir la respuesta (no revela la solución)")
    
    # Clasificación
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    dificultad = models.CharField(max_length=10, choices=DIFICULTAD_CHOICES, default='medio')
    puntos = models.IntegerField(default=10, help_text="Puntos que otorga resolver este reto")
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    # Control de ordenamiento
    orden_prioridad = models.IntegerField(default=0, help_text="Prioridad de ordenamiento (mayor número = más arriba)")
    mostrar_aleatorio = models.BooleanField(default=False, help_text="¿Mostrar este reto en orden aleatorio?")
    
    # Estadísticas
    intentos_totales = models.IntegerField(default=0)
    intentos_exitosos = models.IntegerField(default=0)
    
    # Control de intentos
    max_intentos = models.IntegerField(
        default=3, 
        help_text="Número máximo de intentos permitidos por usuario (1-10)",
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    
    # Imagen del reto
    imagen_reto = models.ImageField(
        upload_to='retos/', 
        blank=True, 
        null=True,
        help_text="Sube una imagen relacionada con el reto (opcional)"
    )
    icono_por_defecto = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[
            ('🧩', '🧩 Puzzle'),
            ('🔢', '🔢 Números'),
            ('🧮', '🧮 Cálculo'),
            ('🎯', '🎯 Objetivo'),
            ('💡', '💡 Idea'),
            ('🎲', '🎲 Dados'),
            ('📊', '📊 Gráficos'),
            ('🔍', '🔍 Búsqueda'),
            ('⚡', '⚡ Rápido'),
            ('🏆', '🏆 Premio'),
            ('🎨', '🎨 Arte'),
            ('🌐', '🌐 Global'),
        ],
        help_text="Selecciona un icono por defecto si no tienes imagen personal"
    )
    
    class Meta:
        verbose_name = "Reto"
        verbose_name_plural = "Retos"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} ({self.get_dificultad_display()})"
    
    def calcular_tasa_exito(self):
        """Calcula el porcentaje de éxito del reto"""
        if self.intentos_totales == 0:
            return 0
        return round((self.intentos_exitosos / self.intentos_totales) * 100, 2)
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas del reto"""
        from juego.models import Intento
        self.intentos_totales = Intento.objects.filter(reto=self).count()
        self.intentos_exitosos = Intento.objects.filter(reto=self, es_correcto=True).count()
        self.save()
    
    def get_intentos_usuario(self, usuario):
        """Obtiene los intentos de un usuario específico para este reto"""
        from juego.models import Intento
        return Intento.objects.filter(usuario=usuario, reto=self).order_by('-fecha_intento')
    
    def get_intentos_restantes(self, usuario):
        """Calcula cuántos intentos le quedan al usuario"""
        intentos_usuario = self.get_intentos_usuario(usuario).count()
        return max(0, self.max_intentos - intentos_usuario)
    
    def usuario_agoto_intentos(self, usuario):
        """Verifica si el usuario ya agotó todos sus intentos"""
        return self.get_intentos_restantes(usuario) == 0
    
    def usuario_resolvio_reto(self, usuario):
        """Verifica si el usuario ya resolvió correctamente el reto"""
        return self.get_intentos_usuario(usuario).filter(es_correcto=True).exists()
    
    def validar_respuesta(self, respuesta_usuario):
        """Valida si la respuesta del usuario es correcta (más flexible)"""
        if not respuesta_usuario:
            return False
        
        # Normalizar respuesta del usuario
        respuesta_normalizada = self._normalizar_respuesta(respuesta_usuario)
        
        # Obtener todas las respuestas correctas posibles
        respuestas_correctas = self.get_respuestas_correctas()
        
        # Verificar si coincide con alguna respuesta correcta
        for respuesta_correcta in respuestas_correctas:
            if self._comparar_respuestas(respuesta_normalizada, respuesta_correcta):
                return True
        
        return False
    
    def get_respuestas_correctas(self):
        """Obtiene todas las respuestas correctas posibles para este reto"""
        respuestas = [self.respuesta_correcta]
        
        # Agregar respuestas alternativas si existen
        respuestas_alternativas = self.respuestas_alternativas.filter(activa=True)
        for alt in respuestas_alternativas:
            respuestas.append(alt.texto)
        
        return respuestas
    
    def _normalizar_respuesta(self, respuesta):
        """Normaliza una respuesta para comparación"""
        if not respuesta:
            return ""
        
        # Convertir a minúsculas
        respuesta = respuesta.lower().strip()
        
        # Remover caracteres especiales y espacios extra
        respuesta = re.sub(r'[^\w\s]', '', respuesta)
        respuesta = re.sub(r'\s+', ' ', respuesta).strip()
        
        return respuesta
    
    def _comparar_respuestas(self, respuesta_usuario, respuesta_correcta):
        """Compara dos respuestas normalizadas"""
        respuesta_correcta_normalizada = self._normalizar_respuesta(respuesta_correcta)
        
        # Comparación exacta
        if respuesta_usuario == respuesta_correcta_normalizada:
            return True
        
        # Comparación por palabras clave (para respuestas más complejas)
        palabras_usuario = set(respuesta_usuario.split())
        palabras_correcta = set(respuesta_correcta_normalizada.split())
        
        # Si hay al menos 80% de coincidencia en palabras clave
        if len(palabras_correcta) > 0:
            coincidencia = len(palabras_usuario.intersection(palabras_correcta)) / len(palabras_correcta)
            if coincidencia >= 0.8:
                return True
        
        return False
    
    def obtener_imagen(self):
        """Retorna la imagen del reto si existe, o el icono por defecto"""
        if self.imagen_reto:
            return self.imagen_reto.url
        return self.icono_por_defecto or '🧩'
    
    def tiene_imagen_personal(self):
        """Verifica si el reto tiene una imagen personal subida"""
        return bool(self.imagen_reto)
    
    def eliminar_imagen_personal(self):
        """Elimina la imagen personal del reto"""
        if self.imagen_reto:
            self.imagen_reto.delete(save=False)
            self.imagen_reto = None
            self.save()


class RespuestaAlternativa(models.Model):
    """Respuestas alternativas correctas para un reto"""
    reto = models.ForeignKey(Reto, on_delete=models.CASCADE, related_name='respuestas_alternativas')
    texto = models.TextField(help_text="Texto de la respuesta alternativa")
    descripcion = models.CharField(max_length=200, blank=True, help_text="Descripción de esta alternativa")
    activa = models.BooleanField(default=True, help_text="¿Esta alternativa está activa?")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Respuesta Alternativa"
        verbose_name_plural = "Respuestas Alternativas"
        ordering = ['fecha_creacion']
    
    def __str__(self):
        return f"{self.reto.titulo} - {self.texto[:50]}..."

class ConfiguracionOrdenamiento(models.Model):
    """Configuración global del ordenamiento de retos"""
    ORDEN_CHOICES = [
        ('fecha', 'Por fecha de creación'),
        ('dificultad', 'Por dificultad'),
        ('puntos', 'Por puntos'),
        ('aleatorio', 'Aleatorio'),
        ('prioridad', 'Por prioridad'),
        ('popularidad', 'Por popularidad'),
    ]
    
    nombre = models.CharField(max_length=50, default="Configuración Principal")
    orden_por_defecto = models.CharField(
        max_length=20, 
        choices=ORDEN_CHOICES, 
        default='fecha',
        help_text="Orden por defecto para mostrar retos"
    )
    incluir_aleatorios = models.BooleanField(
        default=True,
        help_text="¿Incluir retos marcados como aleatorios?"
    )
    max_retos_por_pagina = models.IntegerField(
        default=10,
        help_text="Número máximo de retos por página"
    )
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Configuración de Ordenamiento"
        verbose_name_plural = "Configuraciones de Ordenamiento"
    
    def __str__(self):
        return f"{self.nombre} - {self.get_orden_por_defecto_display()}"
    
    @classmethod
    def get_configuracion_activa(cls):
        """Obtener la configuración activa"""
        try:
            return cls.objects.filter(activo=True).first()
        except:
            return None


# ======== Señales para mantener perfiles y ranking coherentes al borrar Retos ========
@receiver(pre_delete, sender=Reto)
def reto_pre_delete_collect_users(sender, instance: Reto, **kwargs):
    """Antes de borrar un reto, recolectar los usuarios con intentos para actualizar luego."""
    try:
        from juego.models import Intento
        user_ids = list(
            Intento.objects.filter(reto=instance)
            .values_list('usuario_id', flat=True)
            .distinct()
        )
        instance._affected_user_ids = user_ids
    except Exception:
        instance._affected_user_ids = []


@receiver(post_delete, sender=Reto)
def reto_post_delete_update_profiles(sender, instance: Reto, **kwargs):
    """Después de borrar un reto, actualizar perfiles de usuarios afectados y ranking."""
    try:
        from cuentas.models import PerfilUsuario
        from juego.models import Ranking

        user_ids = getattr(instance, '_affected_user_ids', []) or []
        if user_ids:
            perfiles = PerfilUsuario.objects.filter(usuario_id__in=user_ids)
            for perfil in perfiles:
                perfil.actualizar_puntuacion()
        # Refrescar ranking global una sola vez
        Ranking.actualizar_ranking()
    except Exception:
        # En caso de error, no bloquear el borrado
        pass
