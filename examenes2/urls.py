from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('examenes2/', views.examen_list2, name='examenList2'),
    path('examenes2/examenCreate2/', csrf_exempt(views.examen_create2), name='examenCreate2'),
    path('examen2/<int:examen_id>/', views.examen_detail2, name='examenDetail2'),
    path('examen2/<int:examen_id>/delete/', views.examen_delete2, name='examenDelete2'),
]