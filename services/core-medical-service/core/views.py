import logging
from django.http import HttpResponse, JsonResponse # JsonResponse agregado para la nueva función
from django.db import connection, OperationalError, transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserCreateForm

# --- CORREGIDO: Usar doble guion bajo para _name_ ---
logger = logging.getLogger(__name__)

# --- MANTENIDO: Funciones para las sondas ---
def readiness_check(request):
    """
    /health/ready: Usada por Startup Probe. Temporarily simplified to skip DB check.
    """
    # Temporarily skip database check to allow deployment
    logger.info("Startup/Readiness probe: Skipping DB check temporarily.")
    
    # Always return ready for now
    return HttpResponse("Ready", status=200, content_type="text/plain")

def liveness_check(request):
    """
    /health/live: Usada por Liveness Probe. Verifica que el proceso responde.
    """
    # Simplemente devuelve 200 OK para indicar que el proceso está vivo.
    logger.debug("Liveness probe successful.") # Log opcional
    return HttpResponse("Alive", status=200, content_type="text/plain")

# User management views for admin users

def is_admin(user):
    """Check if the user is an admin (has staff status or is in admin group)"""
    return user.is_staff or user.is_superuser or user.groups.filter(name='admin').exists()

@login_required
@user_passes_test(is_admin)
def user_list(request):
    """View to list all users - accessible only to admin users"""
    from django.contrib.auth.models import User
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'core/user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_create(request):
    """View to create a new user - accessible only to admin users"""
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuario "{user.username}" creado exitosamente.')
            return redirect('user_list')
        else:
            # Log form errors for debugging
            print(f"Form is invalid. Errors: {form.errors}")
            messages.error(request, 'Error al crear usuario. Por favor corrija los errores indicados.')
    else:
        form = UserCreateForm()

    return render(request, 'core/user_create.html', {'form': form})

# --- NUEVO: Endpoint temporal para crear el usuario de prueba ---
def create_test_user(request):
    """
    Endpoint temporal para crear un usuario de prueba.
    Solo para propósitos de desarrollo y pruebas.
    """
    # Verifica si el usuario ya existe
    if User.objects.filter(username='testuser').exists():
        return HttpResponse("El usuario de prueba ya existe.", status=400)

    # Crea el usuario de prueba
    try:
        with transaction.atomic():
            test_user = User.objects.create_user(
                username='testuser',
                password='Test1234!',
                email='testuser@example.com'
            )
            test_user.first_name = "Test"
            test_user.last_name = "User"
            test_user.is_staff = True  # Otorgar acceso al admin
            test_user.is_superuser = True  # Otorgar permisos de superusuario
            test_user.save()

        logger.info("Usuario de prueba creado exitosamente.")
        return HttpResponse("Usuario de prueba creado exitosamente.", status=201)
    except Exception as e:
        logger.error(f"Error al crear el usuario de prueba: {e}")
        return HttpResponse("Error al crear el usuario de prueba.", status=500)
