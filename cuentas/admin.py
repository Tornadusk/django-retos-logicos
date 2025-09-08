from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import PerfilUsuario

class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'
    readonly_fields = ['fecha_registro', 'puntuacion_total', 'retos_completados']

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_puntuacion', 'get_nivel')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    def get_puntuacion(self, obj):
        if hasattr(obj, 'perfil'):
            return format_html('<span style="color: #007bff; font-weight: bold;">{} pts</span>', obj.perfil.puntuacion_total)
        return format_html('<span style="color: #6c757d;">0 pts</span>')
    get_puntuacion.short_description = 'Puntuación'
    
    def get_nivel(self, obj):
        if hasattr(obj, 'perfil'):
            return format_html('<span style="background-color: #28a745; color: white; padding: 2px 6px; border-radius: 3px;">Nivel {}</span>', obj.perfil.nivel)
        return format_html('<span style="color: #6c757d;">N/A</span>')
    get_nivel.short_description = 'Nivel'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'puntuacion_badge', 'retos_completados', 'nivel_badge', 'fecha_registro']
    list_filter = ['nivel', 'fecha_registro']
    search_fields = ['usuario__username', 'usuario__email']
    ordering = ['-puntuacion_total']
    readonly_fields = ['fecha_registro', 'puntuacion_total', 'retos_completados']
    actions = ['actualizar_puntuaciones']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('usuario',)
        }),
        ('Estadísticas', {
            'fields': ('puntuacion_total', 'retos_completados', 'nivel')
        }),
        ('Información', {
            'fields': ('fecha_registro',)
        }),
    )
    
    def puntuacion_badge(self, obj):
        if obj.puntuacion_total >= 1000:
            color = '#ffc107'  # Oro
        elif obj.puntuacion_total >= 500:
            color = '#6c757d'  # Plata
        elif obj.puntuacion_total >= 100:
            color = '#fd7e14'  # Bronce
        else:
            color = '#28a745'  # Verde
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-weight: bold;">{} pts</span>',
            color, obj.puntuacion_total
        )
    puntuacion_badge.short_description = 'Puntuación'
    
    def nivel_badge(self, obj):
        colors = {
            1: '#28a745',  # Verde
            2: '#17a2b8',  # Azul
            3: '#ffc107',  # Amarillo
            4: '#fd7e14',  # Naranja
            5: '#dc3545'   # Rojo
        }
        color = colors.get(obj.nivel, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-weight: bold;">Nivel {}</span>',
            color, obj.nivel
        )
    nivel_badge.short_description = 'Nivel'
    
    def actualizar_puntuaciones(self, request, queryset):
        for perfil in queryset:
            perfil.actualizar_puntuacion()
        self.message_user(request, f'Puntuaciones actualizadas para {queryset.count()} perfiles.')
    actualizar_puntuaciones.short_description = "Actualizar puntuaciones"
