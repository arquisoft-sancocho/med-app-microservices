"""medical_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from django.conf import settings
from . import views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # Include app-specific URLs - Core service only
    path('', include('pacientes2.urls')),
    path('consultas/', include('consultas.urls')),
    path('health/', include('core.urls')), # Health checks
    
    # Microservice redirects for seamless navigation
    path('examenes/', views.examenes_redirect, name='examenes_redirect'),
    path('examenes/<path:path>', views.examenes_redirect, name='examenes_redirect_path'),
    path('diagnosticos/', views.diagnosticos_redirect, name='diagnosticos_redirect'),
    path('diagnosticos/<path:path>', views.diagnosticos_redirect, name='diagnosticos_redirect_path'),
    path('cirugias/', views.cirugias_redirect, name='cirugias_redirect'),
    path('cirugias/<path:path>', views.cirugias_redirect, name='cirugias_redirect_path'),
    
    # API endpoints for microservice communication
    path('', include('pacientes2.api_urls')),

    # User management URLs with a dedicated path
    path('users/', core_views.user_list, name='user_list'),
    path('users/create/', core_views.user_create, name='user_create'),

    # Add Django's built-in auth URLs (provides login, logout, password management)
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
