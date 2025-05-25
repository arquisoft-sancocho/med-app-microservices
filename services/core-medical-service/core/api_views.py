"""
API views for core medical service.
These endpoints allow other microservices to access patient and consultation data.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
import requests
import asyncio
import aiohttp
import logging

from pacientes2.models import Paciente2
from consultas.models import ConsultaMedica, Prescripcion
from .serializers import (
    Paciente2Serializer,
    Paciente2BasicSerializer,
    ConsultaSerializer,
    PrescripcionSerializer
)

logger = logging.getLogger(__name__)


class Paciente2ViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for patient data - read-only for microservices"""
    queryset = Paciente2.objects.all()
    serializer_class = Paciente2Serializer

    def get_serializer_class(self):
        """Use basic serializer for list view"""
        if self.action == 'list':
            return Paciente2BasicSerializer
        return Paciente2Serializer


class ConsultaViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for consultation data"""
    queryset = ConsultaMedica.objects.all()
    serializer_class = ConsultaSerializer

    def get_queryset(self):
        """Filter consultations by patient if provided"""
        queryset = ConsultaMedica.objects.all()
        paciente_id = self.request.query_params.get('paciente_id')
        if paciente_id:
            queryset = queryset.filter(paciente_id=paciente_id)
        return queryset


@api_view(['GET'])
def get_patient_basic_info(request, paciente_id):
    """Get basic patient information for other microservices"""
    try:
        paciente = get_object_or_404(Paciente2, id=paciente_id)
        serializer = Paciente2BasicSerializer(paciente)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error getting patient {paciente_id}: {str(e)}")
        return Response(
            {'error': 'Patient not found'},
            status=status.HTTP_404_NOT_FOUND
        )


async def fetch_service_data(session, url, paciente_id):
    """Async helper to fetch data from microservices"""
    try:
        async with session.get(f"{url}/api/patient/{paciente_id}/") as response:
            if response.status == 200:
                return await response.json()
            else:
                logger.warning(f"Service {url} returned status {response.status}")
                return None
    except Exception as e:
        logger.error(f"Error fetching from {url}: {str(e)}")
        return None


@api_view(['GET'])
def get_historia_clinica_completa(request, paciente_id):
    """
    Get complete clinical history for a patient.
    This replaces the monolithic version and calls multiple microservices.
    """
    try:
        # Get basic patient info
        paciente = get_object_or_404(Paciente2, id=paciente_id)
        paciente_data = Paciente2Serializer(paciente).data

        # Get consultations from local database
        consultas = ConsultaMedica.objects.filter(paciente_id=paciente_id)
        consultas_data = ConsultaSerializer(consultas, many=True).data

        # Get prescriptions
        prescripciones = Prescripcion.objects.filter(consulta__paciente_id=paciente_id)
        prescripciones_data = PrescripcionSerializer(prescripciones, many=True).data

        # Prepare async calls to other microservices
        async def fetch_all_services():
            async with aiohttp.ClientSession() as session:
                tasks = []

                # Fetch exams
                if settings.EXAMS_SERVICE_URL:
                    tasks.append(('examenes', fetch_service_data(
                        session, settings.EXAMS_SERVICE_URL, paciente_id
                    )))

                # Fetch diagnoses
                if settings.DIAGNOSIS_SERVICE_URL:
                    tasks.append(('diagnosticos', fetch_service_data(
                        session, settings.DIAGNOSIS_SERVICE_URL, paciente_id
                    )))

                # Fetch surgeries
                if settings.SURGERY_SERVICE_URL:
                    tasks.append(('cirugias', fetch_service_data(
                        session, settings.SURGERY_SERVICE_URL, paciente_id
                    )))

                # Execute all requests concurrently
                results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)

                # Combine results
                service_data = {}
                for i, (service_name, _) in enumerate(tasks):
                    result = results[i]
                    if isinstance(result, Exception):
                        logger.error(f"Error fetching {service_name}: {str(result)}")
                        service_data[service_name] = []
                    else:
                        service_data[service_name] = result or []

                return service_data

        # Execute async calls
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        service_data = loop.run_until_complete(fetch_all_services())

        # Combine all data
        historia_clinica = {
            'paciente': paciente_data,
            'consultas': consultas_data,
            'prescripciones': prescripciones_data,
            'examenes': service_data.get('examenes', []),
            'diagnosticos': service_data.get('diagnosticos', []),
            'cirugias': service_data.get('cirugias', [])
        }

        return Response(historia_clinica)

    except Exception as e:
        logger.error(f"Error getting clinical history for patient {paciente_id}: {str(e)}")
        return Response(
            {'error': 'Error retrieving clinical history'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
