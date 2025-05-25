from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import Cirugia2ViewSet

# Create router for API endpoints
router = DefaultRouter()
router.register(r'cirugias', Cirugia2ViewSet, basename='cirugias')

urlpatterns = [
    path('', include(router.urls)),
]
