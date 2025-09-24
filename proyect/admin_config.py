from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Sum
from retos.models import Reto, Categoria
from retos.admin import RetoAdmin, CategoriaAdmin
from juego.models import Intento, Ranking
from juego.admin import IntentoAdmin, RankingAdmin
from cuentas.models import PerfilUsuario
from cuentas.admin import PerfilUsuarioAdmin, UserAdmin

class CustomAdminSite(admin.AdminSite):
    site_header = "🧩 Retos Lógico Matemáticos"
    site_title = "Admin Retos"
    index_title = "Panel de Administración"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('estadisticas/', self.admin_view(self.estadisticas_view), name='estadisticas'),
            path('reportes/', self.admin_view(self.reportes_view), name='reportes'),
        ]
        return custom_urls + urls
    
    def estadisticas_view(self, request):
        """Vista personalizada para estadísticas del sistema"""
        total_retos = Reto.objects.filter(activo=True).count()
        total_usuarios = PerfilUsuario.objects.count()
        total_intentos = Intento.objects.count()
        intentos_correctos = Intento.objects.filter(es_correcto=True).count()
        
        context = {
            'title': 'Estadísticas del Sistema',
            'total_retos': total_retos,
            'total_usuarios': total_usuarios,
            'total_intentos': total_intentos,
            'intentos_correctos': intentos_correctos,
            'retos_por_dificultad': Reto.objects.filter(activo=True).values('dificultad').annotate(
                count=Count('id')
            ),
            'top_usuarios': PerfilUsuario.objects.order_by('-puntuacion_total')[:5],
            'retos_populares': Reto.objects.filter(activo=True).order_by('-intentos_totales')[:5],
        }
        return render(request, 'admin/estadisticas.html', context)
    
    def reportes_view(self, request):
        """Vista personalizada para reportes"""
        context = {
            'title': 'Reportes del Sistema',
            'intentos_por_fecha': Intento.objects.extra(
                select={'day': 'date(fecha_intento)'}
            ).values('day').annotate(count=Count('id')).order_by('-day')[:30],
        }
        return render(request, 'admin/reportes.html', context)

# Crear instancia personalizada del admin site
admin_site = CustomAdminSite(name='custom_admin')

# Registrar todos los modelos en el admin personalizado
User = get_user_model()
admin_site.register(User, UserAdmin)
admin_site.register(PerfilUsuario, PerfilUsuarioAdmin)
admin_site.register(Reto, RetoAdmin)
admin_site.register(Categoria, CategoriaAdmin)
admin_site.register(Intento, IntentoAdmin)
admin_site.register(Ranking, RankingAdmin)
