from django.urls import path
from . import views

urlpatterns = [
    # Health check endpoints
    path('ready', views.readiness_check, name='readiness_check'),
    path('live', views.liveness_check, name='liveness_check'),
]
