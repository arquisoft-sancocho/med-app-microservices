"""
Views for integrating with microservices.
These views consume APIs from exams, diagnosis, and surgery services.
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from core.microservice_client import microservice_client
from pacientes2.models import Paciente2
import logging

logger = logging.getLogger(__name__)


@login_required
def examenes_list(request):
    """List all exams with microservice integration"""
    try:
        # Get exams from microservice
        url = f"{settings.EXAMS_SERVICE_URL.rstrip('/')}/api/exams/"
        exams = microservice_client._make_request('GET', url)
        if exams is None:
            messages.error(request, "No se pudo conectar al servicio de exámenes")
            exams = []

        return render(request, 'examenes/examenes_list.html', {
            'examenes': exams.get('results', []) if exams else [],
            'service_status': microservice_client.check_service_health(settings.EXAMS_SERVICE_URL)
        })
    except Exception as e:
        logger.error(f"Error loading exams: {e}")
        messages.error(request, "Error al cargar los exámenes")
        return render(request, 'examenes/examenes_list.html', {'examenes': []})


@login_required
def examenes_patient(request, patient_id):
    """List exams for a specific patient"""
    try:
        patient = get_object_or_404(Paciente2, id=patient_id)
        exams = microservice_client.get_patient_exams(patient_id, request)

        return render(request, 'examenes/examenes_patient.html', {
            'patient': patient,
            'examenes': exams,
        })
    except Exception as e:
        logger.error(f"Error loading patient exams: {e}")
        messages.error(request, "Error al cargar los exámenes del paciente")
        return render(request, 'examenes/examenes_patient.html', {
            'patient': None,
            'examenes': []
        })


@login_required
def examenes_detail(request, exam_id):
    """View exam details"""
    try:
        exam = microservice_client.get_exam_detail(exam_id, request)
        if not exam:
            messages.error(request, "Examen no encontrado")
            return render(request, 'examenes/exam_detail.html', {'exam': None})

        return render(request, 'examenes/exam_detail.html', {'exam': exam})
    except Exception as e:
        logger.error(f"Error loading exam detail: {e}")
        messages.error(request, "Error al cargar el detalle del examen")
        return render(request, 'examenes/exam_detail.html', {'exam': None})


@login_required
def diagnosticos_list(request):
    """List all diagnoses"""
    try:
        url = f"{settings.DIAGNOSIS_SERVICE_URL.rstrip('/')}/api/diagnoses/"
        diagnoses = microservice_client._make_request('GET', url)
        if diagnoses is None:
            messages.error(request, "No se pudo conectar al servicio de diagnósticos")
            diagnoses = []

        return render(request, 'diagnosticos/diagnosticos_list.html', {
            'diagnosticos': diagnoses.get('results', []) if diagnoses else []
        })
    except Exception as e:
        logger.error(f"Error loading diagnoses: {e}")
        messages.error(request, "Error al cargar los diagnósticos")
        return render(request, 'diagnosticos/diagnosticos_list.html', {'diagnosticos': []})


@login_required
def diagnosticos_patient(request, patient_id):
    """List diagnoses for a specific patient"""
    try:
        patient = get_object_or_404(Paciente2, id=patient_id)
        diagnoses = microservice_client.get_patient_diagnoses(patient_id, request)

        return render(request, 'diagnosticos/diagnosticos_patient.html', {
            'patient': patient,
            'diagnosticos': diagnoses,
        })
    except Exception as e:
        logger.error(f"Error loading patient diagnoses: {e}")
        messages.error(request, "Error al cargar los diagnósticos del paciente")
        return render(request, 'diagnosticos/diagnosticos_patient.html', {
            'patient': None,
            'diagnosticos': []
        })


@login_required
def cirugias_list(request):
    """List all surgeries"""
    try:
        url = f"{settings.SURGERY_SERVICE_URL.rstrip('/')}/api/surgeries/"
        surgeries = microservice_client._make_request('GET', url)
        if surgeries is None:
            messages.error(request, "No se pudo conectar al servicio de cirugías")
            surgeries = []

        return render(request, 'cirugias/cirugias_list.html', {
            'cirugias': surgeries.get('results', []) if surgeries else []
        })
    except Exception as e:
        logger.error(f"Error loading surgeries: {e}")
        messages.error(request, "Error al cargar las cirugías")
        return render(request, 'cirugias/cirugias_list.html', {'cirugias': []})

        return render(request, 'cirugias/cirugias_list.html', {
            'cirugias': surgeries.get('results', []) if surgeries else []
        })
    except Exception as e:
        logger.error(f"Error loading surgeries: {e}")
        messages.error(request, "Error al cargar las cirugías")
        return render(request, 'cirugias/cirugias_list.html', {'cirugias': []})


@login_required
def cirugias_patient(request, patient_id):
    """List surgeries for a specific patient"""
    try:
        patient = get_object_or_404(Paciente2, id=patient_id)
        surgeries = microservice_client.get_patient_surgeries(patient_id, request)

        return render(request, 'cirugias/cirugias_patient.html', {
            'patient': patient,
            'cirugias': surgeries,
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
