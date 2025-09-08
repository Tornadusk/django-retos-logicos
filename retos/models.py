from django.db import models
from django.contrib.auth.models import User

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
    
    # Clasificación
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    dificultad = models.CharField(max_length=10, choices=DIFICULTAD_CHOICES, default='medio')
    puntos = models.IntegerField(default=10, help_text="Puntos que otorga resolver este reto")
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    # Estadísticas
    intentos_totales = models.IntegerField(default=0)
    intentos_exitosos = models.IntegerField(default=0)
    
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
