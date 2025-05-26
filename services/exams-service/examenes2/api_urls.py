from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import Examen2ViewSet, PublicExamen2ViewSet

router = DefaultRouter()
router.register(r'examenes', Examen2ViewSet)

# Public router for microservice communication
public_router = DefaultRouter()
public_router.register(r'examenes', PublicExamen2ViewSet, basename='public-examenes')

urlpatterns = [
    path('api/', include(router.urls)),
    path('public-api/', include(public_router.urls)),
]
