from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.contrib import messages
from .models import Reto, Categoria, ConfiguracionOrdenamiento
from juego.models import Intento, Ranking

def home(request):
    """Vista principal del sitio"""
    # Estadísticas generales
    total_retos = Reto.objects.filter(activo=True).count()
    total_usuarios = Ranking.objects.count()
    
    # Retos más populares (con más intentos)
    retos_populares = Reto.objects.filter(activo=True).order_by('-intentos_totales')[:5]
    
    # Top 5 del ranking
    top_ranking = Ranking.objects.all()[:5]
    
    context = {
        'total_retos': total_retos,
        'total_usuarios': total_usuarios,
        'retos_populares': retos_populares,
        'top_ranking': top_ranking,
    }
    return render(request, 'retos/home.html', context)

@login_required
def dashboard(request):
    """Dashboard del usuario con sus estadísticas"""
    usuario = request.user
    
    # Estadísticas del usuario
    intentos_usuario = Intento.objects.filter(usuario=usuario)
    intentos_correctos = intentos_usuario.filter(es_correcto=True)
    
    # Retos completados por dificultad
    retos_por_dificultad = {}
    for dificultad, _ in Reto.DIFICULTAD_CHOICES:
        retos_por_dificultad[dificultad] = intentos_correctos.filter(
            reto__dificultad=dificultad
        ).count()
    
    # Últimos intentos
    ultimos_intentos = intentos_usuario.select_related('reto')[:10]
    
    # Posición en el ranking
    try:
        ranking_usuario = Ranking.objects.get(usuario=usuario)
        posicion_ranking = ranking_usuario.posicion
    except Ranking.DoesNotExist:
        posicion_ranking = None
    
    # Retos disponibles (que no ha intentado)
    retos_intentados = intentos_usuario.values_list('reto_id', flat=True)
    retos_disponibles = Reto.objects.filter(activo=True).exclude(
        id__in=retos_intentados
    ).order_by('dificultad', 'puntos')[:10]
    
    context = {
        'intentos_totales': intentos_usuario.count(),
        'intentos_correctos': intentos_correctos.count(),
        'puntuacion_total': usuario.perfil.puntuacion_total,
        'retos_completados': usuario.perfil.retos_completados,
        'retos_por_dificultad': retos_por_dificultad,
        'ultimos_intentos': ultimos_intentos,
        'posicion_ranking': posicion_ranking,
        'retos_disponibles': retos_disponibles,
    }
    return render(request, 'retos/dashboard.html', context)

class ListaRetosView(ListView):
    """Vista para listar todos los retos disponibles"""
    model = Reto
    template_name = 'retos/lista_retos.html'
    context_object_name = 'retos'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Reto.objects.filter(activo=True).select_related('categoria')
        
        # Filtros
        dificultad = self.request.GET.get('dificultad')
        categoria = self.request.GET.get('categoria')
        busqueda = self.request.GET.get('busqueda')
        
        if dificultad:
            queryset = queryset.filter(dificultad=dificultad)
        
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
        
        if busqueda:
            queryset = queryset.filter(
                Q(titulo__icontains=busqueda) |
                Q(descripcion__icontains=busqueda) |
                Q(enunciado__icontains=busqueda)
            )
        
        # Aplicar ordenamiento
        orden = self.request.GET.get('orden', 'fecha')
        
        if orden == 'fecha':
            queryset = queryset.order_by('-fecha_creacion')
        elif orden == 'dificultad':
            queryset = queryset.order_by('dificultad', 'puntos')
        elif orden == 'puntos':
            queryset = queryset.order_by('-puntos')
        elif orden == 'prioridad':
            queryset = queryset.order_by('-orden_prioridad', '-fecha_creacion')
        elif orden == 'popularidad':
            queryset = queryset.order_by('-intentos_totales')
        elif orden == 'aleatorio':
            import random
            queryset = list(queryset)
            random.shuffle(queryset)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['dificultades'] = Reto.DIFICULTAD_CHOICES
        
        # Agregar timestamp para cache busting del JavaScript
        import time
        context['timestamp'] = int(time.time())
        
        # Si el usuario está logueado, marcar qué retos ya intentó
        if self.request.user.is_authenticated:
            retos_intentados = Intento.objects.filter(
                usuario=self.request.user
            ).values_list('reto_id', flat=True)
            context['retos_intentados'] = retos_intentados
        
        return context

class DetalleRetoView(LoginRequiredMixin, DetailView):
    """Vista para mostrar el detalle de un reto"""
    model = Reto
    template_name = 'retos/detalle_reto.html'
    context_object_name = 'reto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reto = self.get_object()
        usuario = self.request.user
        
        # Obtener intentos del usuario para este reto
        intentos_usuario = reto.get_intentos_usuario(usuario)
        context['intentos_usuario'] = intentos_usuario
        context['intentos_restantes'] = reto.get_intentos_restantes(usuario)
        context['agoto_intentos'] = reto.usuario_agoto_intentos(usuario)
        context['resolvio_reto'] = reto.usuario_resolvio_reto(usuario)
        context['ya_intentado'] = intentos_usuario.exists()
        
        # Estadísticas del reto
        context['tasa_exito'] = reto.calcular_tasa_exito()
        
        return context

@login_required
def intentar_reto(request, pk):
    """Vista para procesar un intento de resolución de reto"""
    reto = get_object_or_404(Reto, pk=pk, activo=True)
    
    # Verificar si ya resolvió el reto
    if reto.usuario_resolvio_reto(request.user):
        messages.info(request, 'Ya has resuelto correctamente este reto.')
        return redirect('retos:detalle_reto', pk=pk)
    
    # Verificar si agotó los intentos
    if reto.usuario_agoto_intentos(request.user):
        messages.warning(request, 'Has agotado todos tus intentos para este reto.')
        return redirect('retos:detalle_reto', pk=pk)
    
    if request.method == 'POST':
        respuesta_usuario = request.POST.get('respuesta', '').strip()
        
        if not respuesta_usuario:
            messages.error(request, 'Debes proporcionar una respuesta.')
            return redirect('retos:detalle_reto', pk=pk)
        
        # Verificar si la respuesta es correcta (validación flexible)
        es_correcto = reto.validar_respuesta(respuesta_usuario)
        
        # Crear el intento
        intento = Intento.objects.create(
            usuario=request.user,
            reto=reto,
            respuesta_usuario=respuesta_usuario,
            es_correcto=es_correcto
        )
        
        # Actualizar ranking
        Ranking.actualizar_ranking()
        
        # Calcular intentos restantes
        intentos_restantes = reto.get_intentos_restantes(request.user)
        
        if es_correcto:
            messages.success(request, f'¡Correcto! Has ganado {intento.puntuacion_obtenida} puntos.')
        else:
            if intentos_restantes > 0:
                messages.error(request, f'Respuesta incorrecta. Te quedan {intentos_restantes} intentos.')
            else:
                messages.error(request, 'Respuesta incorrecta. Has agotado todos tus intentos.')
        
        return redirect('retos:detalle_reto', pk=pk)
    
    return redirect('retos:detalle_reto', pk=pk)
