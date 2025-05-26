from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import Diagnostico2ViewSet, Tratamiento2ViewSet, PublicDiagnostico2ViewSet, PublicTratamiento2ViewSet

router = DefaultRouter()
router.register(r'diagnosticos', Diagnostico2ViewSet)
router.register(r'tratamientos', Tratamiento2ViewSet)

# Public router for microservice communication
public_router = DefaultRouter()
public_router.register(r'diagnosticos', PublicDiagnostico2ViewSet, basename='public-diagnosticos')
public_router.register(r'tratamientos', PublicTratamiento2ViewSet, basename='public-tratamientos')

urlpatterns = [
    path('api/', include(router.urls)),
    path('public-api/', include(public_router.urls)),
]
