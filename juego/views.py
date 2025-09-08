from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import Count, Sum, Case, When, F, FloatField
from django.db import models
from .models import Ranking, Intento
from retos.models import Reto

class RankingView(ListView):
    """Vista para mostrar el ranking de usuarios"""
    model = Ranking
    template_name = 'juego/ranking.html'
    context_object_name = 'ranking'
    paginate_by = 20
    
    def get_queryset(self):
        return Ranking.objects.select_related('usuario').order_by('posicion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales del ranking
        total_usuarios = Ranking.objects.count()
        total_puntos = Ranking.objects.aggregate(
            total=Sum('puntuacion_total')
        )['total'] or 0
        
        # Top 3 usuarios
        top_3 = Ranking.objects.select_related('usuario')[:3]
        
        # Posición del usuario actual si está logueado
        if self.request.user.is_authenticated:
            try:
                ranking_usuario = Ranking.objects.get(usuario=self.request.user)
                context['ranking_usuario'] = ranking_usuario
            except Ranking.DoesNotExist:
                context['ranking_usuario'] = None
        
        context.update({
            'total_usuarios': total_usuarios,
            'total_puntos': total_puntos,
            'top_3': top_3,
        })
        
        return context

@login_required
def mis_estadisticas(request):
    """Vista para mostrar las estadísticas detalladas del usuario"""
    usuario = request.user
    
    # Intentos del usuario
    intentos = Intento.objects.filter(usuario=usuario).select_related('reto')
    intentos_correctos = intentos.filter(es_correcto=True)
    
    # Estadísticas por dificultad
    stats_por_dificultad = {}
    for dificultad, nombre in Reto.DIFICULTAD_CHOICES:
        retos_dificultad = intentos_correctos.filter(reto__dificultad=dificultad)
        stats_por_dificultad[dificultad] = {
            'nombre': nombre,
            'completados': retos_dificultad.count(),
            'puntos': retos_dificultad.aggregate(
                total=Sum('puntuacion_obtenida')
            )['total'] or 0,
        }
    
    # Progreso por categoría
    stats_por_categoria = {}
    categorias = Reto.objects.values_list('categoria__nombre', flat=True).distinct()
    for categoria in categorias:
        if categoria:
            retos_categoria = intentos_correctos.filter(reto__categoria__nombre=categoria)
            stats_por_categoria[categoria] = {
                'completados': retos_categoria.count(),
                'puntos': retos_categoria.aggregate(
                    total=Sum('puntuacion_obtenida')
                )['total'] or 0,
            }
    
    # Historial de intentos recientes
    historial = intentos.order_by('-fecha_intento')[:20]
    
    # Posición en el ranking
    try:
        ranking_usuario = Ranking.objects.get(usuario=usuario)
        posicion = ranking_usuario.posicion
    except Ranking.DoesNotExist:
        posicion = None
    
    context = {
        'intentos_totales': intentos.count(),
        'intentos_correctos': intentos_correctos.count(),
        'puntuacion_total': usuario.perfil.puntuacion_total,
        'retos_completados': usuario.perfil.retos_completados,
        'stats_por_dificultad': stats_por_dificultad,
        'stats_por_categoria': stats_por_categoria,
        'historial': historial,
        'posicion_ranking': posicion,
    }
    
    return render(request, 'juego/mis_estadisticas.html', context)

@login_required
def progreso_global(request):
    """Vista para mostrar el progreso global del sistema"""
    # Estadísticas generales
    total_retos = Reto.objects.filter(activo=True).count()
    total_usuarios = Ranking.objects.count()
    total_intentos = Intento.objects.count()
    intentos_correctos = Intento.objects.filter(es_correcto=True).count()
    
    # Retos más difíciles (menor tasa de éxito)
    retos_dificiles = Reto.objects.filter(activo=True).annotate(
        tasa_exito=models.Case(
            models.When(intentos_totales=0, then=0),
            default=models.F('intentos_exitosos') * 100.0 / models.F('intentos_totales'),
            output_field=models.FloatField()
        )
    ).order_by('tasa_exito')[:10]
    
    # Retos más populares
    retos_populares = Reto.objects.filter(activo=True).order_by('-intentos_totales')[:10]
    
    # Distribución por dificultad
    distribucion_dificultad = {}
    for dificultad, nombre in Reto.DIFICULTAD_CHOICES:
        retos_dificultad = Reto.objects.filter(dificultad=dificultad, activo=True)
        distribucion_dificultad[dificultad] = {
            'nombre': nombre,
            'cantidad': retos_dificultad.count(),
            'intentos': Intento.objects.filter(reto__dificultad=dificultad).count(),
        }
    
    context = {
        'total_retos': total_retos,
        'total_usuarios': total_usuarios,
        'total_intentos': total_intentos,
        'intentos_correctos': intentos_correctos,
        'tasa_exito_global': round((intentos_correctos / total_intentos * 100) if total_intentos > 0 else 0, 2),
        'retos_dificiles': retos_dificiles,
        'retos_populares': retos_populares,
        'distribucion_dificultad': distribucion_dificultad,
    }
    
    return render(request, 'juego/progreso_global.html', context)
