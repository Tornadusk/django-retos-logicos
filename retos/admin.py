from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Categoria, Reto, ConfiguracionOrdenamiento, RespuestaAlternativa

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


class RespuestaAlternativaInline(admin.TabularInline):
    """Inline para gestionar respuestas alternativas desde el admin de Reto"""
    model = RespuestaAlternativa
    extra = 1
    fields = ['texto', 'descripcion', 'activa']
    ordering = ['fecha_creacion']


class RetoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'dificultad_badge', 'puntos', 'max_intentos', 'activo_badge', 'tasa_exito', 'fecha_creacion']
    list_filter = ['dificultad', 'categoria', 'activo', 'max_intentos', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'enunciado']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion', 'intentos_totales', 'intentos_exitosos', 'tasa_exito_calculada']
    actions = ['activar_retos', 'desactivar_retos', 'actualizar_estadisticas', 'cambiar_max_intentos']
    inlines = [RespuestaAlternativaInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'categoria', 'dificultad', 'puntos'),
            'description': '''
            <div style="background: #f8f9fa; padding: 10px; border-left: 4px solid #007bff; margin: 10px 0;">
                <strong>📝 CAMPOS PARA EL USUARIO FINAL:</strong><br>
                • <strong>titulo:</strong> Nombre del reto que ven los usuarios (ej: "El problema de los sombreros")<br>
                • <strong>descripcion:</strong> Descripción general del reto para los usuarios (ej: "Un clásico problema de lógica deductiva")<br>
                • <strong>categoria, dificultad, puntos:</strong> Clasificación y puntuación del reto
            </div>
            '''
        }),
        ('Contenido del Reto', {
            'fields': ('enunciado', 'respuesta_correcta', 'explicacion'),
            'description': '''
            <div style="background: #f8f9fa; padding: 10px; border-left: 4px solid #28a745; margin: 10px 0;">
                <strong>🎯 CAMPOS DE VALIDACIÓN:</strong><br>
                • <strong>enunciado:</strong> El problema completo que debe resolver el usuario<br>
                • <strong>respuesta_correcta:</strong> La respuesta principal que valida el sistema (ej: "blanco")<br>
                • <strong>explicacion:</strong> Explicación de la solución que se muestra al usuario
            </div>
            '''
        }),
        ('Respuestas Alternativas', {
            'fields': (),
            'description': '''
            <div style="background: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin: 10px 0;">
                <strong>🔄 VARIACIONES DE RESPUESTA (gestionadas abajo):</strong><br>
                • <strong>texto:</strong> La variación específica que acepta el sistema (ej: "BLANCO", "blanco.")<br>
                • <strong>descripcion:</strong> Nota para el admin sobre el tipo de variación (ej: "En mayúsculas", "Con punto final")<br>
                <em>Estas variaciones se agregan en la sección de abajo para mayor flexibilidad en las respuestas.</em>
            </div>
            '''
        }),
        ('Configuración de Intentos', {
            'fields': ('max_intentos',),
            'description': 'Número máximo de intentos permitidos por usuario para este reto'
        }),
        ('Configuración General', {
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
    
    def cambiar_max_intentos(self, request, queryset):
        """Acción personalizada para cambiar max_intentos de múltiples retos"""
        from django import forms
        from django.shortcuts import render
        
        class CambiarIntentosForm(forms.Form):
            max_intentos = forms.IntegerField(
                min_value=1, 
                max_value=10,
                initial=3,
                help_text="Número de intentos permitidos (1-10)"
            )
        
        if 'apply' in request.POST:
            form = CambiarIntentosForm(request.POST)
            if form.is_valid():
                max_intentos = form.cleaned_data['max_intentos']
                updated = queryset.update(max_intentos=max_intentos)
                self.message_user(
                    request, 
                    f'Se actualizaron {updated} retos con {max_intentos} intentos máximo.'
                )
                return
        else:
            form = CambiarIntentosForm()
        
        context = {
            'form': form,
            'queryset': queryset,
            'action_name': 'cambiar_max_intentos',
            'title': 'Cambiar número máximo de intentos'
        }
        return render(request, 'admin/retos/reto/cambiar_intentos.html', context)
    cambiar_max_intentos.short_description = "Cambiar número de intentos"


class RespuestaAlternativaAdmin(admin.ModelAdmin):
    """Admin para RespuestaAlternativa"""
    list_display = ['reto', 'texto_preview', 'descripcion', 'activa', 'fecha_creacion']
    list_filter = ['activa', 'reto', 'fecha_creacion']
    search_fields = ['texto', 'descripcion', 'reto__titulo']
    ordering = ['-fecha_creacion']
    
    fieldsets = (
        ('Información de la Variación', {
            'fields': ('reto', 'texto', 'descripcion', 'activa'),
            'description': '''
            <div style="background: #f8f9fa; padding: 10px; border-left: 4px solid #ffc107; margin: 10px 0;">
                <strong>🔄 CAMPOS DE RESPUESTA ALTERNATIVA:</strong><br>
                • <strong>texto:</strong> La variación específica que acepta el sistema (ej: "BLANCO", "17 minutos")<br>
                • <strong>descripcion:</strong> Nota para el admin sobre el tipo de variación (ej: "En mayúsculas", "Con unidad")<br>
                • <strong>activa:</strong> Si esta variación está disponible para validación<br>
                <em>Estas variaciones se agregan a la respuesta_correcta principal del reto.</em>
            </div>
            '''
        }),
    )
    
    def texto_preview(self, obj):
        return obj.texto[:50] + "..." if len(obj.texto) > 50 else obj.texto
    texto_preview.short_description = "Texto"

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


# Registrar modelos en el admin
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Reto, RetoAdmin)
admin.site.register(RespuestaAlternativa, RespuestaAlternativaAdmin)
admin.site.register(ConfiguracionOrdenamiento, ConfiguracionOrdenamientoAdmin)
