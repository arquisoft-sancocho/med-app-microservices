from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import Paciente2APIViewSet

router = DefaultRouter()
router.register(r'patients', Paciente2APIViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
