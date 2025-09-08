from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Categoria, Reto, ConfiguracionOrdenamiento

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'color_preview', 'retos_count']
    list_filter = ['nombre']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']
    
    def color_preview(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            obj.color,
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def retos_count(self, obj):
        count = obj.reto_set.filter(activo=True).count()
        return format_html('<span style="color: #007bff; font-weight: bold;">{}</span>', count)
    retos_count.short_description = 'Retos Activos'

class RetoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'dificultad_badge', 'puntos', 'activo_badge', 'tasa_exito', 'fecha_creacion']
    list_filter = ['dificultad', 'categoria', 'activo', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'enunciado']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion', 'intentos_totales', 'intentos_exitosos', 'tasa_exito_calculada']
    actions = ['activar_retos', 'desactivar_retos', 'actualizar_estadisticas']
    
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
            'fields': ('intentos_totales', 'intentos_exitosos', 'tasa_exito_calculada'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    def dificultad_badge(self, obj):
        colors = {
            'facil': '#28a745',
            'medio': '#ffc107', 
            'dificil': '#fd7e14',
            'experto': '#dc3545'
        }
        color = colors.get(obj.dificultad, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_dificultad_display()
        )
    dificultad_badge.short_description = 'Dificultad'
    
    def activo_badge(self, obj):
        if obj.activo:
            return format_html('<span style="color: #28a745; font-weight: bold;">✓ Activo</span>')
        else:
            return format_html('<span style="color: #dc3545; font-weight: bold;">✗ Inactivo</span>')
    activo_badge.short_description = 'Estado'
    
    def tasa_exito(self, obj):
        tasa = obj.calcular_tasa_exito()
        color = '#28a745' if tasa >= 50 else '#ffc107' if tasa >= 25 else '#dc3545'
        return format_html('<span style="color: {}; font-weight: bold;">{}%</span>', color, tasa)
    tasa_exito.short_description = 'Tasa Éxito'
    
    def tasa_exito_calculada(self, obj):
        return f"{obj.calcular_tasa_exito()}%"
    tasa_exito_calculada.short_description = 'Tasa de Éxito'
    
    def activar_retos(self, request, queryset):
        updated = queryset.update(activo=True)
        self.message_user(request, f'{updated} retos activados correctamente.')
    activar_retos.short_description = "Activar retos seleccionados"
    
    def desactivar_retos(self, request, queryset):
        updated = queryset.update(activo=False)
        self.message_user(request, f'{updated} retos desactivados correctamente.')
    desactivar_retos.short_description = "Desactivar retos seleccionados"
    
    def actualizar_estadisticas(self, request, queryset):
        for reto in queryset:
            reto.actualizar_estadisticas()
        self.message_user(request, f'Estadísticas actualizadas para {queryset.count()} retos.')
    actualizar_estadisticas.short_description = "Actualizar estadísticas"

class ConfiguracionOrdenamientoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'orden_por_defecto', 'max_retos_por_pagina', 'incluir_aleatorios', 'activo']
    list_filter = ['orden_por_defecto', 'activo', 'incluir_aleatorios']
    search_fields = ['nombre']
    fieldsets = (
        ('Configuración General', {
            'fields': ('nombre', 'activo')
        }),
        ('Ordenamiento', {
            'fields': ('orden_por_defecto', 'incluir_aleatorios')
        }),
        ('Paginación', {
            'fields': ('max_retos_por_pagina',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Asegurar que solo haya una configuración activa"""
        if obj.activo:
            # Desactivar otras configuraciones
            ConfiguracionOrdenamiento.objects.filter(activo=True).exclude(id=obj.id).update(activo=False)
        super().save_model(request, obj, form, change)
