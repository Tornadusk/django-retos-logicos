from django.urls import path
from . import views

app_name = 'juego'

urlpatterns = [
    path('ranking/', views.RankingView.as_view(), name='ranking'),
    path('mis-estadisticas/', views.mis_estadisticas, name='mis_estadisticas'),
    path('progreso-global/', views.progreso_global, name='progreso_global'),
]
