from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario

class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'
    readonly_fields = ['fecha_registro', 'puntuacion_total', 'retos_completados']

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_puntuacion')
    
    def get_puntuacion(self, obj):
        if hasattr(obj, 'perfil'):
            return obj.perfil.puntuacion_total
        return 0
    get_puntuacion.short_description = 'Puntuación'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'puntuacion_total', 'retos_completados', 'nivel', 'fecha_registro']
    list_filter = ['nivel', 'fecha_registro']
    search_fields = ['usuario__username', 'usuario__email']
    ordering = ['-puntuacion_total']
    readonly_fields = ['fecha_registro', 'puntuacion_total', 'retos_completados']
    
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
