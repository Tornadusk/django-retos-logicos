from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.contrib import messages
from .models import Reto, Categoria
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
        
        return queryset.order_by('dificultad', 'puntos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['dificultades'] = Reto.DIFICULTAD_CHOICES
        
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
        
        # Verificar si el usuario ya intentó este reto
        try:
            intento = Intento.objects.get(usuario=usuario, reto=reto)
            context['intento'] = intento
            context['ya_intentado'] = True
        except Intento.DoesNotExist:
            context['ya_intentado'] = False
        
        # Estadísticas del reto
        context['tasa_exito'] = reto.calcular_tasa_exito()
        
        return context

@login_required
def intentar_reto(request, pk):
    """Vista para procesar un intento de resolución de reto"""
    reto = get_object_or_404(Reto, pk=pk, activo=True)
    
    # Verificar si ya intentó este reto
    if Intento.objects.filter(usuario=request.user, reto=reto).exists():
        messages.warning(request, 'Ya has intentado resolver este reto.')
        return redirect('retos:detalle_reto', pk=pk)
    
    if request.method == 'POST':
        respuesta_usuario = request.POST.get('respuesta', '').strip()
        
        if not respuesta_usuario:
            messages.error(request, 'Debes proporcionar una respuesta.')
            return redirect('retos:detalle_reto', pk=pk)
        
        # Verificar si la respuesta es correcta (comparación simple)
        es_correcto = respuesta_usuario.lower() == reto.respuesta_correcta.lower()
        
        # Crear el intento
        intento = Intento.objects.create(
            usuario=request.user,
            reto=reto,
            respuesta_usuario=respuesta_usuario,
            es_correcto=es_correcto
        )
        
        # Actualizar ranking
        Ranking.actualizar_ranking()
        
        if es_correcto:
            messages.success(request, f'¡Correcto! Has ganado {intento.puntuacion_obtenida} puntos.')
        else:
            messages.error(request, 'Respuesta incorrecta. Inténtalo de nuevo.')
        
        return redirect('retos:detalle_reto', pk=pk)
    
    return redirect('retos:detalle_reto', pk=pk)
