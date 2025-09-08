from django.contrib import admin
from .models import Intento, Ranking

@admin.register(Intento)
class IntentoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'reto', 'es_correcto', 'puntuacion_obtenida', 'fecha_intento']
    list_filter = ['es_correcto', 'fecha_intento', 'reto__dificultad', 'reto__categoria']
    search_fields = ['usuario__username', 'reto__titulo', 'respuesta_usuario']
    ordering = ['-fecha_intento']
    readonly_fields = ['fecha_intento', 'puntuacion_obtenida']
    
    fieldsets = (
        ('Información del Intento', {
            'fields': ('usuario', 'reto', 'respuesta_usuario', 'es_correcto')
        }),
        ('Resultados', {
            'fields': ('puntuacion_obtenida', 'tiempo_respuesta', 'fecha_intento')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usuario', 'reto')

@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ['posicion', 'usuario', 'puntuacion_total', 'retos_completados', 'fecha_actualizacion']
    list_filter = ['fecha_actualizacion']
    search_fields = ['usuario__username']
    ordering = ['posicion']
    readonly_fields = ['fecha_actualizacion']
    
    def has_add_permission(self, request):
        return False  # El ranking se actualiza automáticamente
    
    def has_change_permission(self, request, obj=None):
        return False  # El ranking se actualiza automáticamente
