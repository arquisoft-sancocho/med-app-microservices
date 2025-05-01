from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('cirugias/', views.cirugia_list, name='cirugiaList'),
    path('cirugias/cirugiaCreate2/', csrf_exempt(views.cirugia_create), name='cirugiaCreate'),
    path('cirugia/<int:cirugia_id>/', views.cirugia_detail, name='cirugiaDetail'),
    path('cirugia/<int:cirugia_id>/delete/', views.cirugia_delete, name='cirugiaDelete'),
]