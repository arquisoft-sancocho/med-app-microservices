from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views
from . import jwt_views
from . import permissions_api

# API Router for microservice endpoints
router = DefaultRouter()
router.register(r'patients', api_views.Paciente2ViewSet, basename='patients')
router.register(r'consultations', api_views.ConsultaViewSet, basename='consultations')

urlpatterns = [
    # Health check endpoints
    path('ready', views.readiness_check, name='readiness_check'),
    path('live', views.liveness_check, name='liveness_check'),

    # JWT Authentication endpoints
    path('auth/login/', jwt_views.jwt_login, name='jwt-login'),
    path('auth/validate/', jwt_views.jwt_validate, name='jwt-validate'),
    path('auth/refresh/', jwt_views.jwt_refresh, name='jwt-refresh'),

    # API endpoints for microservices
    path('api/', include(router.urls)),
    path('api/patient/<int:paciente_id>/basic/', api_views.get_patient_basic_info, name='patient-basic'),
    path('api/patient/<int:paciente_id>/historia-clinica/', api_views.get_historia_clinica_completa, name='historia-clinica'),
    
    # Permissions setup endpoints
    path('api/setup-permissions/', permissions_api.setup_permissions_endpoint, name='setup-permissions'),
    path('api/permissions-status/', permissions_api.permissions_status, name='permissions-status'),
]
