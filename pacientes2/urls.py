from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('pacientes2/', views.paciente_list2, name='pacienteList2'),
    path('pacientes2/pacienteCreate2/', csrf_exempt(views.paciente_create2), name='pacienteCreate2'),
    path('paciente2/<int:paciente_id>/', views.paciente_detail2, name='pacienteDetail2'),
    path('paciente2/<int:paciente_id>/historiaClinica', views.historia_clinica_view, name='historiaClinica'),
    path('paciente2/<int:paciente_id>/informacionCritica', views.informacion_critica, name='informacionCritica'),
    path('paciente2/<int:paciente_id>/delete/', views.paciente_delete2, name='pacienteDelete2'),
    path('paciente2/<int:paciente_id>/edit/', views.paciente_edit2, name='pacienteEdit2'),
]