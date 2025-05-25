from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

# API Router for microservice endpoints
router = DefaultRouter()
router.register(r'patients', api_views.Paciente2ViewSet, basename='patients')
router.register(r'consultations', api_views.ConsultaViewSet, basename='consultations')

urlpatterns = [
    # Health check endpoints
    path('ready', views.readiness_check, name='readiness_check'),
    path('live', views.liveness_check, name='liveness_check'),

    # API endpoints for microservices
    path('api/', include(router.urls)),
    path('api/patient/<int:paciente_id>/basic/', api_views.get_patient_basic_info, name='patient-basic'),
    path('api/patient/<int:paciente_id>/historia-clinica/', api_views.get_historia_clinica_completa, name='historia-clinica'),
]
