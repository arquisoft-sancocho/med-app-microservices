"""
Views for integrating with microservices.
These views consume APIs from exams, diagnosis, and surgery services.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from core.microservice_client import microservice_client
from core.permissions import (
    require_examenes_access, require_diagnosticos_access, require_cirugias_access,
    can_add_examenes, can_add_diagnosticos, can_add_cirugias,
    get_user_permissions_context, require_add_permission
)
from pacientes2.models import Paciente2
import logging
import json

logger = logging.getLogger(__name__)


@require_examenes_access
def examenes_list(request):
    """List all exams with microservice integration"""
    try:
        # Get exams from microservice
        url = f"{settings.EXAMS_SERVICE_URL.rstrip('/')}/public-api/examenes/"
        exams = microservice_client._make_request('GET', url)
        if exams is None:
            messages.error(request, "No se pudo conectar al servicio de exámenes")
            exams = []

        # Get user permissions context
        permissions_context = get_user_permissions_context(request.user)

        return render(request, 'examenes/examenes_list.html', {
            'examenes': exams.get('results', []) if exams else [],
            'service_status': microservice_client.check_service_health(settings.EXAMS_SERVICE_URL),
            **permissions_context
        })
    except Exception as e:
        logger.error(f"Error loading exams: {e}")
        messages.error(request, "Error al cargar los exámenes")
        return render(request, 'examenes/examenes_list.html', {'examenes': []})


@require_examenes_access
def examenes_patient(request, patient_id):
    """List exams for a specific patient"""
    try:
        patient = get_object_or_404(Paciente2, id=patient_id)
        exams = microservice_client.get_patient_exams(patient_id, request)

        # Get user permissions context
        permissions_context = get_user_permissions_context(request.user)

        return render(request, 'examenes/examenes_patient.html', {
            'patient': patient,
            'examenes': exams,
            **permissions_context
        })
    except Exception as e:
        logger.error(f"Error loading patient exams: {e}")
        messages.error(request, "Error al cargar los exámenes del paciente")
        return render(request, 'examenes/examenes_patient.html', {
            'patient': None,
            'examenes': []
        })


@require_examenes_access
def examenes_detail(request, exam_id):
    """View exam details"""
    try:
        exam = microservice_client.get_exam_detail(exam_id, request)
        if not exam:
            messages.error(request, "Examen no encontrado")
            return render(request, 'examenes/exam_detail.html', {'exam': None})

        # Get user permissions context
        permissions_context = get_user_permissions_context(request.user)

        return render(request, 'examenes/exam_detail.html', {
            'exam': exam,
            **permissions_context
        })
    except Exception as e:
        logger.error(f"Error loading exam detail: {e}")
        messages.error(request, "Error al cargar el detalle del examen")
        return render(request, 'examenes/exam_detail.html', {'exam': None})


@require_diagnosticos_access
def diagnosticos_list(request):
    """List all diagnoses"""
    try:
        url = f"{settings.DIAGNOSIS_SERVICE_URL.rstrip('/')}/public-api/diagnosticos/"
        diagnoses = microservice_client._make_request('GET', url)
        if diagnoses is None:
            messages.error(request, "No se pudo conectar al servicio de diagnósticos")
            diagnoses = []

        # Get user permissions context
        permissions_context = get_user_permissions_context(request.user)

        return render(request, 'diagnosticos/diagnosticos_list.html', {
            'diagnosticos': diagnoses.get('results', []) if diagnoses else [],
            **permissions_context
        })
    except Exception as e:
        logger.error(f"Error loading diagnoses: {e}")
        messages.error(request, "Error al cargar los diagnósticos")
        return render(request, 'diagnosticos/diagnosticos_list.html', {'diagnosticos': []})


@require_diagnosticos_access
def diagnosticos_patient(request, patient_id):
    """List diagnoses for a specific patient"""
    try:
        patient = get_object_or_404(Paciente2, id=patient_id)
        diagnoses = microservice_client.get_patient_diagnoses(patient_id, request)

        # Get user permissions context
        permissions_context = get_user_permissions_context(request.user)

        return render(request, 'diagnosticos/diagnosticos_patient.html', {
            'patient': patient,
            'diagnosticos': diagnoses,
            **permissions_context
        })
    except Exception as e:
        logger.error(f"Error loading patient diagnoses: {e}")
        messages.error(request, "Error al cargar los diagnósticos del paciente")
        return render(request, 'diagnosticos/diagnosticos_patient.html', {
            'patient': None,
            'diagnosticos': []
        })


@require_cirugias_access
def cirugias_list(request):
    """List all surgeries"""
    try:
        url = f"{settings.SURGERY_SERVICE_URL.rstrip('/')}/api/public/cirugias/"
        surgeries = microservice_client._make_request('GET', url)
        if surgeries is None:
            messages.error(request, "No se pudo conectar al servicio de cirugías")
            surgeries = []

        # Get user permissions context
        permissions_context = get_user_permissions_context(request.user)

        return render(request, 'cirugias/cirugias_list.html', {
            'cirugias': surgeries.get('results', []) if surgeries else [],
            **permissions_context
        })
    except Exception as e:
        logger.error(f"Error loading surgeries: {e}")
        messages.error(request, "Error al cargar las cirugías")
        return render(request, 'cirugias/cirugias_list.html', {'cirugias': []})


@require_cirugias_access
def cirugias_patient(request, patient_id):
    """List surgeries for a specific patient"""
    try:
        patient = get_object_or_404(Paciente2, id=patient_id)
        surgeries = microservice_client.get_patient_surgeries(patient_id, request)

        # Get user permissions context
        permissions_context = get_user_permissions_context(request.user)

        return render(request, 'cirugias/cirugias_patient.html', {
            'patient': patient,
            'cirugias': surgeries,
            **permissions_context
        })
    except Exception as e:
        logger.error(f"Error loading patient surgeries: {e}")
        messages.error(request, "Error al cargar las cirugías del paciente")
        return render(request, 'cirugias/cirugias_patient.html', {
            'patient': None,
            'cirugias': []
        })


@login_required
def services_status(request):
    """Get microservices status"""
    status = microservice_client.get_services_status()

    if request.headers.get('Accept') == 'application/json':
        return JsonResponse(status)

    return render(request, 'core/services_status.html', {'services': status})


# Views for adding new records
from django.views.decorators.http import require_http_methods


@require_add_permission(can_add_examenes)
@require_http_methods(["GET", "POST"])
def examenes_add(request):
    """Add new exam"""
    if request.method == 'GET':
        # Get patients for dropdown
        patients = Paciente2.objects.all()
        permissions_context = get_user_permissions_context(request.user)
        
        return render(request, 'examenes/examenes_add.html', {
            'patients': patients,
            **permissions_context
        })
    
    elif request.method == 'POST':
        try:
            # Prepare exam data
            exam_data = {
                'nombre': request.POST.get('nombre'),
                'descripcion': request.POST.get('descripcion'),
                'paciente_id': request.POST.get('paciente_id'),
                'fecha_examen': request.POST.get('fecha_examen'),
                'resultado': request.POST.get('resultado', ''),
                'observaciones': request.POST.get('observaciones', ''),
            }
            
            # Send to microservice
            url = f"{settings.EXAMS_SERVICE_URL.rstrip('/')}/api/examenes/"
            response = microservice_client._make_request('POST', url, json=exam_data)
            
            if response:
                messages.success(request, "Examen creado exitosamente")
                return redirect('examenes_redirect')
            else:
                messages.error(request, "Error al crear el examen")
                
        except Exception as e:
            logger.error(f"Error creating exam: {e}")
            messages.error(request, "Error al procesar la solicitud")
        
        # If error, reload form with data
        patients = Paciente2.objects.all()
        permissions_context = get_user_permissions_context(request.user)
        
        return render(request, 'examenes/examenes_add.html', {
            'patients': patients,
            'form_data': request.POST,
            **permissions_context
        })


@require_add_permission(can_add_diagnosticos)
@require_http_methods(["GET", "POST"])
def diagnosticos_add(request):
    """Add new diagnosis"""
    if request.method == 'GET':
        # Get patients for dropdown
        patients = Paciente2.objects.all()
        permissions_context = get_user_permissions_context(request.user)
        
        return render(request, 'diagnosticos/diagnosticos_add.html', {
            'patients': patients,
            **permissions_context
        })
    
    elif request.method == 'POST':
        try:
            # Prepare diagnosis data
            diagnosis_data = {
                'nombre': request.POST.get('nombre'),
                'descripcion': request.POST.get('descripcion'),
                'paciente_id': request.POST.get('paciente_id'),
                'fecha_diagnostico': request.POST.get('fecha_diagnostico'),
                'codigo_cie': request.POST.get('codigo_cie', ''),
                'tratamiento': request.POST.get('tratamiento', ''),
                'observaciones': request.POST.get('observaciones', ''),
            }
            
            # Send to microservice
            url = f"{settings.DIAGNOSIS_SERVICE_URL.rstrip('/')}/api/diagnosticos/"
            response = microservice_client._make_request('POST', url, json=diagnosis_data)
            
            if response:
                messages.success(request, "Diagnóstico creado exitosamente")
                return redirect('diagnosticos_redirect')
            else:
                messages.error(request, "Error al crear el diagnóstico")
                
        except Exception as e:
            logger.error(f"Error creating diagnosis: {e}")
            messages.error(request, "Error al procesar la solicitud")
        
        # If error, reload form with data
        patients = Paciente2.objects.all()
        permissions_context = get_user_permissions_context(request.user)
        
        return render(request, 'diagnosticos/diagnosticos_add.html', {
            'patients': patients,
            'form_data': request.POST,
            **permissions_context
        })


@require_add_permission(can_add_cirugias)
@require_http_methods(["GET", "POST"])
def cirugias_add(request):
    """Add new surgery"""
    if request.method == 'GET':
        # Get patients for dropdown
        patients = Paciente2.objects.all()
        permissions_context = get_user_permissions_context(request.user)
        
        return render(request, 'cirugias/cirugias_add.html', {
            'patients': patients,
            **permissions_context
        })
    
    elif request.method == 'POST':
        try:
            # Prepare surgery data
            surgery_data = {
                'nombre': request.POST.get('nombre'),
                'descripcion': request.POST.get('descripcion'),
                'paciente_id': request.POST.get('paciente_id'),
                'fecha_programada': request.POST.get('fecha_programada'),
                'fecha_realizada': request.POST.get('fecha_realizada') or None,
                'duracion_minutos': request.POST.get('duracion_minutos') or None,
                'estado': request.POST.get('estado', 'programada'),
                'observaciones': request.POST.get('observaciones', ''),
                'complicaciones': request.POST.get('complicaciones', ''),
            }
            
            # Send to microservice
            url = f"{settings.SURGERY_SERVICE_URL.rstrip('/')}/api/cirugias/"
            response = microservice_client._make_request('POST', url, json=surgery_data)
            
            if response:
                messages.success(request, "Cirugía creada exitosamente")
                return redirect('cirugias_redirect')
            else:
                messages.error(request, "Error al crear la cirugía")
                
        except Exception as e:
            logger.error(f"Error creating surgery: {e}")
            messages.error(request, "Error al procesar la solicitud")
        
        # If error, reload form with data
        patients = Paciente2.objects.all()
        permissions_context = get_user_permissions_context(request.user)
        
        return render(request, 'cirugias/cirugias_add.html', {
            'patients': patients,
            'form_data': request.POST,
            **permissions_context
        })


@login_required
def permission_denied(request):
    """Permission denied page"""
    return render(request, 'core/permission_denied.html', {
        'user_groups': list(request.user.groups.values_list('name', flat=True)) if request.user.is_authenticated else []
    })
