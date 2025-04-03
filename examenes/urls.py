from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('examenes/', views.examen_list, name='examenList'),
    path('examenes/examenCreate/', csrf_exempt(views.examen_create), name='examenCreate'),
    path('examen/<int:examen_id>/', views.examen_detail, name='examenDetail'),
]