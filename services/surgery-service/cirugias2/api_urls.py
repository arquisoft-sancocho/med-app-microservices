from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import Cirugia2ViewSet, PublicCirugia2ViewSet

# Create router for API endpoints
router = DefaultRouter()
router.register(r'cirugias', Cirugia2ViewSet, basename='cirugias')

# Public router for microservice communication
public_router = DefaultRouter()
public_router.register(r'cirugias', PublicCirugia2ViewSet, basename='public-cirugias')

urlpatterns = [
    path('', include(router.urls)),
    path('public/', include(public_router.urls)),
]
