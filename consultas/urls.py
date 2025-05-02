from django.urls import path
from . import views

urlpatterns = [
    path('consultas/', views.consulta_list, name='consultaList'),
    path('consultas/crear/', views.consulta_create, name='consultaCreate'),
    path('consulta/<int:consulta_id>/', views.consulta_detail, name='consultaDetail'),
    path('consulta/<int:consulta_id>/add_prescripcion/', views.add_prescripcion, name='addPrescripcion'),
    path('consulta/<int:consulta_id>/delete/', views.consulta_delete, name='consultaDelete'),
]