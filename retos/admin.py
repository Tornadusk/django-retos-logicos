from django.contrib import admin
from .models import Categoria, Reto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'color']
    list_filter = ['nombre']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']

@admin.register(Reto)
class RetoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'dificultad', 'puntos', 'activo', 'intentos_totales', 'intentos_exitosos', 'fecha_creacion']
    list_filter = ['dificultad', 'categoria', 'activo', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'enunciado']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion', 'intentos_totales', 'intentos_exitosos']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'categoria', 'dificultad', 'puntos')
        }),
        ('Contenido del Reto', {
            'fields': ('enunciado', 'respuesta_correcta', 'explicacion')
        }),
        ('Configuración', {
            'fields': ('activo', 'creado_por')
        }),
        ('Estadísticas', {
            'fields': ('intentos_totales', 'intentos_exitosos'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo reto
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)
