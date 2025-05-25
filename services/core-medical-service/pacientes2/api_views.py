from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Paciente2
from .serializers import Paciente2Serializer, Paciente2BasicSerializer

class Paciente2APIViewSet(viewsets.ModelViewSet):
    queryset = Paciente2.objects.all()
    serializer_class = Paciente2Serializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def basic_info(self, request, pk=None):
        """Endpoint para obtener información básica de un paciente"""
        try:
            paciente = self.get_object()
            serializer = Paciente2BasicSerializer(paciente)
            return Response(serializer.data)
        except Paciente2.DoesNotExist:
            return Response(
                {'error': 'Paciente no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def validate_patient(self, request):
        """Endpoint para validar si un paciente existe"""
        patient_id = request.data.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'patient_id es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        exists = Paciente2.objects.filter(id=patient_id).exists()
        return Response({'exists': exists, 'patient_id': patient_id})

    @action(detail=False, methods=['post'])
    def bulk_validate(self, request):
        """Endpoint para validar múltiples pacientes"""
        patient_ids = request.data.get('patient_ids', [])
        if not isinstance(patient_ids, list):
            return Response(
                {'error': 'patient_ids debe ser una lista'},
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_ids = list(
            Paciente2.objects.filter(id__in=patient_ids).values_list('id', flat=True)
        )

        return Response({
            'existing_ids': existing_ids,
            'non_existing_ids': [pid for pid in patient_ids if pid not in existing_ids]
        })
