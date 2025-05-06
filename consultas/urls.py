from django.urls import path
from . import views

urlpatterns = [
    path('', views.consulta_list, name='consultaList'),
    path('consultaCreate/', views.consulta_create, name='consultaCreate'),
    path('<int:consulta_id>/', views.consulta_detail, name='consultaDetail'),
    path('<int:consulta_id>/add_prescripcion/', views.add_prescripcion, name='addPrescripcion'),
    path('<int:consulta_id>/delete/', views.consulta_delete, name='consultaDelete'),
]
