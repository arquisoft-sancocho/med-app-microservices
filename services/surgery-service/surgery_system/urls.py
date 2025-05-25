"""
URL configuration for surgery_system project - Surgery Microservice
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Health check endpoints
    path('health/', include('core.urls')),

    # API endpoints for surgery operations
    path('api/', include('cirugias2.api_urls')),
]
