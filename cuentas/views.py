from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import PerfilUsuario
from juego.models import Ranking

def registro(request):
    """Vista para el registro de nuevos usuarios"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}!')
            
            # Autenticar y loguear al usuario
            login(request, user)
            
            # Crear entrada en el ranking
            Ranking.actualizar_ranking()
            
            return redirect('retos:dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'cuentas/registro.html', {'form': form})

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
    if request.method == 'POST':
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_confirmar = request.POST.get('password_confirmar')
        
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
