from django.contrib import admin
from django.utils.html import format_html
from .models import Intento, Ranking

class IntentoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'reto', 'resultado_badge', 'puntuacion_obtenida', 'fecha_intento']
    list_filter = ['es_correcto', 'fecha_intento', 'reto__dificultad', 'reto__categoria']
    search_fields = ['usuario__username', 'reto__titulo', 'respuesta_usuario']
    ordering = ['-fecha_intento']
    readonly_fields = ['fecha_intento', 'puntuacion_obtenida']
    actions = ['recalcular_puntuaciones']
    
    fieldsets = (
        ('Información del Intento', {
            'fields': ('usuario', 'reto', 'respuesta_usuario', 'es_correcto')
        }),
        ('Resultados', {
            'fields': ('puntuacion_obtenida', 'tiempo_respuesta', 'fecha_intento')
        }),
    )
    
    def resultado_badge(self, obj):
        if obj.es_correcto:
            return format_html('<span style="color: #28a745; font-weight: bold;">✓ Correcto</span>')
        else:
            return format_html('<span style="color: #dc3545; font-weight: bold;">✗ Incorrecto</span>')
    resultado_badge.short_description = 'Resultado'
    
    def recalcular_puntuaciones(self, request, queryset):
        for intento in queryset:
            if intento.es_correcto:
                intento.puntuacion_obtenida = intento.calcular_puntuacion()
                intento.save()
        self.message_user(request, f'Puntuaciones recalculadas para {queryset.count()} intentos.')
    recalcular_puntuaciones.short_description = "Recalcular puntuaciones"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usuario', 'reto')

class RankingAdmin(admin.ModelAdmin):
    list_display = ['posicion_badge', 'usuario', 'puntuacion_total', 'retos_completados', 'fecha_actualizacion']
    list_filter = ['fecha_actualizacion']
    search_fields = ['usuario__username']
    ordering = ['posicion']
    readonly_fields = ['fecha_actualizacion', 'posicion', 'puntuacion_total', 'retos_completados']
    actions = ['actualizar_ranking_manual']
    
    def posicion_badge(self, obj):
        if obj.posicion <= 3:
            colors = {1: '#ffc107', 2: '#6c757d', 3: '#fd7e14'}
            color = colors.get(obj.posicion, '#007bff')
            icon = '🥇' if obj.posicion == 1 else '🥈' if obj.posicion == 2 else '🥉'
            return format_html(
                '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px;">{} #{}</span>',
                color, icon, obj.posicion
            )
        else:
            return format_html('<span style="color: #6c757d;">#{}</span>', obj.posicion)
    posicion_badge.short_description = 'Posición'
    
    def actualizar_ranking_manual(self, request, queryset):
        Ranking.actualizar_ranking()
        self.message_user(request, 'Ranking actualizado correctamente.')
    actualizar_ranking_manual.short_description = "Actualizar ranking manualmente"
    
    def has_add_permission(self, request):
        return False  # El ranking se actualiza automáticamente
    
    def has_change_permission(self, request, obj=None):
        return False  # El ranking se actualiza automáticamente
