from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
     # Ruta para la Sonda de Disponibilidad
    path('health/ready', views.readiness_check, name='readiness_check'),
    # Ruta para la Sonda de Actividad
    path('health/live', views.liveness_check, name='liveness_check'),

    
]
