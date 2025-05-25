from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Diagnostico2, Tratamiento2
from .serializers import (
    Diagnostico2Serializer, DiagnosticoCreateSerializer,
    Tratamiento2Serializer, TratamientoCreateSerializer
)

class Diagnostico2ViewSet(viewsets.ModelViewSet):
    queryset = Diagnostico2.objects.all()
    serializer_class = Diagnostico2Serializer

    def get_serializer_class(self):
        if self.action == 'create':
            return DiagnosticoCreateSerializer
        return Diagnostico2Serializer

    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        """Get all diagnoses for a specific patient"""
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'patient_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        diagnoses = self.queryset.filter(paciente_id=patient_id)
        serializer = self.get_serializer(diagnoses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search diagnoses by patient name or diagnosis name"""
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'q parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        diagnoses = self.queryset.filter(
            Q(nombre__icontains=query) |
            Q(paciente_nombre__icontains=query) |
            Q(resultados_obtenidos__icontains=query)
        )
        serializer = self.get_serializer(diagnoses, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new diagnosis"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        diagnosis = serializer.save()

        # Return full diagnosis data
        response_serializer = Diagnostico2Serializer(diagnosis)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class Tratamiento2ViewSet(viewsets.ModelViewSet):
    queryset = Tratamiento2.objects.all()
    serializer_class = Tratamiento2Serializer

    def get_serializer_class(self):
        if self.action == 'create':
            return TratamientoCreateSerializer
        return Tratamiento2Serializer

    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        """Get all treatments for a specific patient"""
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'patient_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        treatments = self.queryset.filter(paciente_id=patient_id)
        serializer = self.get_serializer(treatments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_diagnosis(self, request):
        """Get all treatments for a specific diagnosis"""
        diagnosis_id = request.query_params.get('diagnosis_id')
        if not diagnosis_id:
            return Response(
                {'error': 'diagnosis_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        treatments = self.queryset.filter(diagnostico_id=diagnosis_id)
        serializer = self.get_serializer(treatments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active treatments (ongoing treatments)"""
        from django.utils import timezone
        today = timezone.now().date()

        treatments = self.queryset.filter(
            fecha_inicio__lte=today,
            fecha_fin__gte=today
        )
        serializer = self.get_serializer(treatments, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new treatment"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        treatment = serializer.save()

        # Return full treatment data
        response_serializer = Tratamiento2Serializer(treatment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
