from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from .models import PerfilUsuario
from .forms import RegistroForm, LoginForm, PerfilForm
from juego.models import Ranking

def registro(request):
    """Vista para el registro de nuevos usuarios"""
    # Si el usuario ya está logueado, redirigir al dashboard
    if request.user.is_authenticated:
        messages.info(request, 'Ya tienes una sesión activa. Para crear otra cuenta, primero cierra sesión.')
        return redirect('retos:dashboard')
    
    if request.method == 'POST':
        print(f"DEBUG: POST request recibido, CSRF token: {request.POST.get('csrfmiddlewaretoken', 'NO ENCONTRADO')}")
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'¡Cuenta creada para {username}! Se envió un email de confirmación a {email}')
            
            # Autenticar y loguear al usuario
            login(request, user)
            
            # Crear entrada en el ranking
            Ranking.actualizar_ranking()
            
            return redirect('retos:dashboard')
    else:
        form = RegistroForm()
    
    return render(request, 'cuentas/registro.html', {'form': form})

class CustomLoginView(LoginView):
    """Vista personalizada de login que permite email o username"""
    form_class = LoginForm
    template_name = 'cuentas/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Redirigir usuarios ya autenticados"""
        if request.user.is_authenticated:
            messages.info(request, 'Ya tienes una sesión activa. Para cambiar de cuenta, primero cierra sesión.')
            return redirect('retos:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Mensaje de bienvenida personalizado"""
        username = form.cleaned_data.get('username')
        user = form.get_user()
        
        # Mostrar mensaje de bienvenida
        if user.first_name:
            messages.success(self.request, f'¡Bienvenido de vuelta, {user.first_name}!')
        else:
            messages.success(self.request, f'¡Bienvenido de vuelta, {username}!')
        
        return super().form_valid(form)

@login_required
def perfil(request):
    """Vista para mostrar y editar el perfil del usuario"""
    usuario = request.user
    
    if request.method == 'POST':
        # Actualizar información del usuario
        usuario.first_name = request.POST.get('first_name', '')
        usuario.last_name = request.POST.get('last_name', '')
        usuario.email = request.POST.get('email', '')
        usuario.save()
        
        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('cuentas:perfil')
    
    # Obtener estadísticas del usuario
    try:
        ranking_usuario = Ranking.objects.get(usuario=usuario)
        posicion_ranking = ranking_usuario.posicion
    except Ranking.DoesNotExist:
        posicion_ranking = None
    
    context = {
        'usuario': usuario,
        'perfil': usuario.perfil,
        'posicion_ranking': posicion_ranking,
    }
    
    return render(request, 'cuentas/perfil.html', context)

@login_required
def cambiar_password(request):
    """Vista para cambiar la contraseña del usuario"""
    # Si es administrador, redirigir al panel admin
    if request.user.is_staff:
        messages.info(request, 'Como administrador, debes cambiar tu contraseña desde el Panel de Administración.')
        return redirect('admin:password_change')
    
    if request.method == 'POST':
        password_actual = request.POST.get('old_password')
        password_nueva = request.POST.get('new_password1')
        password_confirmar = request.POST.get('new_password2')
        
        # Verificar contraseña actual
        if not request.user.check_password(password_actual):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return redirect('cuentas:cambiar_password')
        
        # Verificar que las nuevas contraseñas coincidan
        if password_nueva != password_confirmar:
            messages.error(request, 'Las nuevas contraseñas no coinciden.')
            return redirect('cuentas:cambiar_password')
        
        # Cambiar contraseña
        request.user.set_password(password_nueva)
        request.user.save()
        
        messages.success(request, 'Contraseña cambiada correctamente.')
        return redirect('cuentas:perfil')
    
    return render(request, 'cuentas/cambiar_password.html')

@login_required
def editar_perfil(request):
    """Vista para editar la foto de perfil del usuario"""
    perfil = request.user.perfil
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        
        # Si se quiere eliminar la foto
        if 'eliminar_foto' in request.POST:
            perfil.eliminar_foto_personal()
            messages.success(request, 'Foto eliminada correctamente.')
            return redirect('cuentas:editar_perfil')
        
        if form.is_valid():
            # Procesar opciones de foto
            opcion_foto = request.POST.get('opcion_foto')
            
            if opcion_foto == 'personal':
                # Si se subió una foto, usar la foto personal
                if 'foto_perfil' in request.FILES:
                    perfil.foto_perfil = request.FILES['foto_perfil']
                    perfil.avatar_por_defecto = None  # Limpiar avatar por defecto
                # Si no hay foto nueva pero ya tenía una, mantenerla
            elif opcion_foto == 'avatar':
                # Usar avatar por defecto
                perfil.foto_perfil = None  # Limpiar foto personal
                if 'avatar_por_defecto' in request.POST:
                    perfil.avatar_por_defecto = request.POST['avatar_por_defecto'] or None
            elif opcion_foto == 'sin_foto':
                # Sin foto ni avatar
                perfil.foto_perfil = None
                perfil.avatar_por_defecto = None
            
            perfil.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('cuentas:perfil')
    else:
        form = PerfilForm(instance=perfil)
    
    context = {
        'form': form,
        'perfil': perfil,
    }
    
    return render(request, 'cuentas/editar_perfil.html', context)
