from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import Diagnostico2ViewSet, Tratamiento2ViewSet

router = DefaultRouter()
router.register(r'diagnosticos', Diagnostico2ViewSet)
router.register(r'tratamientos', Tratamiento2ViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
