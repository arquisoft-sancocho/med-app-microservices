from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('diagnosticos/', views.diagnostico_list, name='diagnosticoList'),
    path('diagnosticos/diagnosticoCreate/', csrf_exempt(views.diagnostico_create), name='diagnosticoCreate'),
    path('diagnostico/<int:diagnostico_id>/', views.diagnostico_detail, name='diagnosticoDetail'),
    path('diagnosticoUpdate/<int:diagnostico_id>/', views.diagnostico_update, name='diagnosticoUpdate'),
]