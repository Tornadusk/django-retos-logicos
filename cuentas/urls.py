from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'cuentas'

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='cuentas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
]
