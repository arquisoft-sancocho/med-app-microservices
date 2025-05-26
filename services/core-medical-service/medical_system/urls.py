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
from core import microservice_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('test-url/', views.test_url_resolution, name='test_url'),  # Temporarily removed

    # Microservice API integration views (replacing redirects with API calls)
    path('examenes/', microservice_views.examenes_list, name='examenes_redirect'),
    path('diagnosticos/', microservice_views.diagnosticos_list, name='diagnosticos_redirect'),
    path('cirugias/', microservice_views.cirugias_list, name='cirugias_redirect'),

    # Add new record views
    path('examenes/add/', microservice_views.examenes_add, name='examenes_add'),
    path('diagnosticos/add/', microservice_views.diagnosticos_add, name='diagnosticos_add'),
    path('cirugias/add/', microservice_views.cirugias_add, name='cirugias_add'),

    # Permission denied page
    path('permission-denied/', microservice_views.permission_denied, name='permission_denied'),

    # Main index view
    path('', views.index, name='index'),

    # Include app-specific URLs - Core service only
    path('', include('pacientes2.urls')),
    path('consultas/', include('consultas.urls')),
    path('health/', include('core.urls')), # Health checks

    # Microservice API integration views (for API calls)
    path('api/examenes/', microservice_views.examenes_list, name='examenes_list'),
    path('api/examenes/patient/<int:patient_id>/', microservice_views.examenes_patient, name='examenes_patient'),
    path('api/examenes/detail/<int:exam_id>/', microservice_views.examenes_detail, name='examenes_detail'),

    path('api/diagnosticos/', microservice_views.diagnosticos_list, name='diagnosticos_list'),
    path('api/diagnosticos/patient/<int:patient_id>/', microservice_views.diagnosticos_patient, name='diagnosticos_patient'),

    path('api/cirugias/', microservice_views.cirugias_list, name='cirugias_list'),
    path('api/cirugias/patient/<int:patient_id>/', microservice_views.cirugias_patient, name='cirugias_patient'),

    # Microservice status endpoint
    path('services/status/', microservice_views.services_status, name='services_status'),

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
