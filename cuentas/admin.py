from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django import forms
from .models import PerfilUsuario

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = '__all__'
        widgets = {
            'nivel': forms.NumberInput(attrs={'min': 1, 'max': 100}),
        }

class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'
    readonly_fields = ['fecha_registro', 'puntuacion_total', 'retos_completados']

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_puntuacion', 'get_nivel', 'view_action')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    # Permitir borrado masivo, pero filtrando al propio usuario en la ejecución
    def get_actions(self, request):
        return super().get_actions(request)

    def has_delete_permission(self, request, obj=None):
        # Impedir que el usuario autenticado se elimine a sí mismo
        if obj is not None and obj.pk == request.user.pk:
            return False
        return super().has_delete_permission(request, obj)

    def delete_queryset(self, request, queryset):
        # Excluir al usuario autenticado en el borrado masivo
        inicial = queryset.count()
        queryset = queryset.exclude(pk=request.user.pk)
        omitidos = inicial - queryset.count()
        if omitidos:
            self.message_user(request, f"Se omitió tu propio usuario en la eliminación masiva ({omitidos} elemento/s).")
        return super().delete_queryset(request, queryset)

    # Ruta adicional para ver un usuario en modo solo lectura
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/view/',
                self.admin_site.admin_view(self.user_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_view",
            ),
        ]
        return custom_urls + urls

    def user_view(self, request, object_id):
        obj = self.get_object(request, object_id)
        context = dict(
            self.admin_site.each_context(request),
            opts=self.model._meta,
            original=obj,
            title=f"Ver usuario: {obj.username}",
            has_view_permission=True,
        )
        return TemplateResponse(request, 'admin/cuentas/user_view.html', context)

    def view_action(self, obj):
        url = reverse(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_view",
            args=[obj.pk],
        )
        return format_html('<a class="button" href="{}">Ver</a>', url)
    view_action.short_description = 'Ver'
    view_action.allow_tags = True
    
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

# Re-register UserAdmin con el modelo swappeado
User = get_user_model()
try:
    admin.site.unregister(User)
except Exception:
    pass
admin.site.register(User, UserAdmin)

class PerfilUsuarioAdmin(admin.ModelAdmin):
    form = PerfilUsuarioForm
    list_display = ['usuario', 'puntuacion_badge', 'retos_completados', 'nivel_badge', 'fecha_registro']
    list_filter = ['nivel', 'fecha_registro']
    search_fields = ['usuario__username', 'usuario__email']
    ordering = ['-puntuacion_total']
    actions = []
    # Mostrar como listado informativo: sin enlaces de edición
    list_display_links = None
    # Bloquear creación directa desde este admin.
    # Los perfiles deben crearse junto con el User (signal o inline).
    can_delete = False
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si estamos editando un perfil existente
            return ['fecha_registro', 'puntuacion_total', 'retos_completados']
        else:  # Si estamos creando un nuevo perfil
            return ['fecha_registro', 'puntuacion_total', 'retos_completados']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Si estamos creando un nuevo perfil, filtrar usuarios que ya tienen perfil
        if not obj:
            form.base_fields['usuario'].queryset = get_user_model().objects.filter(perfil__isnull=True)
            # Asegurar que el campo nivel sea editable
            if 'nivel' in form.base_fields:
                form.base_fields['nivel'].widget.attrs['readonly'] = False
        return form
    
    def get_fieldsets(self, request, obj=None):
        if obj:  # Si estamos editando un perfil existente
            return (
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
        else:  # Si estamos creando un nuevo perfil
            return (
                ('Usuario', {
                    'fields': ('usuario',)
                }),
                ('Configuración Inicial', {
                    'fields': ('nivel',),
                    'description': 'Configura el nivel inicial del usuario. Las estadísticas (puntuación y retos completados) se calcularán automáticamente cuando el usuario comience a resolver retos.'
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
    
    def has_add_permission(self, request):
        # Evitar "Add" aquí: use el inline en Usuario o cree el usuario (que crea el perfil)
        return False

    def has_delete_permission(self, request, obj=None):
        # Permitir borrado para que al eliminar un Usuario, el Perfil se elimine en cascada
        # (necesario para que no aparezca el error de permisos en el borrado del User).
        return True

    def has_change_permission(self, request, obj=None):
        # Sin edición desde esta sección; usar el inline en Usuarios
        return False

    def get_actions(self, request):
        # Ocultar la acción masiva "Delete selected" en el changelist de PerfilUsuario
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Ocultar el botón de eliminar en la vista de edición del Perfil
        extra_context = extra_context or {}
        extra_context['show_delete'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
