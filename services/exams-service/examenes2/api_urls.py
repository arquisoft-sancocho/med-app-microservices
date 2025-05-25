from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import Examen2ViewSet

router = DefaultRouter()
router.register(r'examenes', Examen2ViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
