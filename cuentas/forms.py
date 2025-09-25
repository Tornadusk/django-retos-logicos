from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario

class RegistroForm(UserCreationForm):
    """Formulario personalizado de registro que incluye email"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar widgets de contraseña
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })

    def clean_email(self):
        """Validar que el email sea único"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email

    def save(self, commit=True):
        """Guardar el usuario con email"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    """Formulario personalizado de login que permite email o username"""
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario o Email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )

    def clean_username(self):
        """Permitir login con email o username"""
        username = self.cleaned_data.get('username')
        
        # Si contiene @, es un email
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                raise forms.ValidationError('No existe una cuenta con este email.')
        else:
            # Es un username normal
            return username

class PerfilForm(forms.ModelForm):
    """Formulario para editar el perfil de usuario con opciones de foto"""
    
    class Meta:
        model = PerfilUsuario
        fields = ['foto_perfil', 'avatar_por_defecto']
        widgets = {
            'foto_perfil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'avatar_por_defecto': forms.Select(attrs={
                'class': 'form-select'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer el campo de foto opcional
        self.fields['foto_perfil'].required = False
        self.fields['avatar_por_defecto'].required = False
        
        # Añadir opción vacía para avatar por defecto
        self.fields['avatar_por_defecto'].choices = [
            ('', 'Sin avatar (usar 👤 por defecto)')
        ] + list(self.fields['avatar_por_defecto'].choices[1:])
    
    def clean_foto_perfil(self):
        """Validar la foto de perfil"""
        foto = self.cleaned_data.get('foto_perfil')
        if foto:
            # Validar tamaño (máximo 5MB)
            if foto.size > 5 * 1024 * 1024:
                raise forms.ValidationError('La foto no puede ser mayor a 5MB.')
            
            # Validar formato
            if not foto.content_type.startswith('image/'):
                raise forms.ValidationError('Solo se permiten archivos de imagen.')
        
        return foto
