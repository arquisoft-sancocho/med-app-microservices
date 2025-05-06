from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.diagnostico_list, name='diagnosticoList'),
    path('diagnosticoCreate/', csrf_exempt(views.diagnostico_create), name='diagnosticoCreate'),
    path('<int:diagnostico_id>/', views.diagnostico_detail, name='diagnosticoDetail'),
    path('<int:diagnostico_id>/add_tratamiento/', views.add_tratamiento, name='addTratamiento'),
    path('<int:diagnostico_id>/delete/', views.diagnostico_delete, name='diagnosticoDelete'),
]
