from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.cirugia_list, name='cirugiaList'),
    path('cirugiaCreate/', csrf_exempt(views.cirugia_create), name='cirugiaCreate'),
    path('<int:cirugia_id>/', views.cirugia_detail, name='cirugiaDetail'),
    path('<int:cirugia_id>/delete/', views.cirugia_delete, name='cirugiaDelete'),
    path('<int:cirugia_id>/edit/', views.cirugia_edit, name='cirugiaEdit'),
]
