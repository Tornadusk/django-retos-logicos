from django.urls import path
from . import views

app_name = 'retos'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('retos/', views.ListaRetosView.as_view(), name='lista_retos'),
    path('reto/<int:pk>/', views.DetalleRetoView.as_view(), name='detalle_reto'),
    path('reto/<int:pk>/intentar/', views.intentar_reto, name='intentar_reto'),
]
