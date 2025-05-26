from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from .models import Cirugia2
from .serializers import Cirugia2Serializer, Cirugia2BasicSerializer

class Cirugia2ViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Surgery operations in the surgery microservice
    """
    queryset = Cirugia2.objects.all()
    serializer_class = Cirugia2Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = Cirugia2.objects.all()

        # Filter by patient ID
        patient_id = self.request.query_params.get('patient_id', None)
        if patient_id:
            queryset = queryset.filter(paciente_id=patient_id)

        # Filter by surgery type
        tipo = self.request.query_params.get('tipo', None)
        if tipo:
            queryset = queryset.filter(tipo=tipo)

        # Filter by post-operative status
        estado = self.request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estado_postoperatorio=estado)

        return queryset.order_by('-fecha')

    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        """Get surgeries for a specific patient"""
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'patient_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        surgeries = self.get_queryset().filter(paciente_id=patient_id)
        serializer = self.get_serializer(surgeries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get surgeries by type"""
        surgery_type = request.query_params.get('type')
        if not surgery_type:
            return Response(
                {'error': 'type parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        surgeries = self.get_queryset().filter(tipo=surgery_type)
        serializer = self.get_serializer(surgeries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search surgeries by name, result, or complications"""
        query = request.query_params.get('q')
        if not query:
            return Response(
                {'error': 'q parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        surgeries = self.get_queryset().filter(
            Q(nombre__icontains=query) |
            Q(resultado__icontains=query) |
            Q(complicaciones__icontains=query) |
            Q(notas_quirurgicas__icontains=query)
        )
        serializer = self.get_serializer(surgeries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get surgery statistics"""
        total = self.get_queryset().count()
        by_type = {}
        by_status = {}

        for surgery in self.get_queryset():
            # Count by type
            tipo_display = surgery.get_tipo_display()
            by_type[tipo_display] = by_type.get(tipo_display, 0) + 1

            # Count by status
            status_display = surgery.get_estado_postoperatorio_display()
            by_status[status_display] = by_status.get(status_display, 0) + 1

        return Response({
            'total_surgeries': total,
            'by_type': by_type,
            'by_status': by_status
        })

class PublicCirugia2ViewSet(viewsets.ReadOnlyModelViewSet):
    """Public API for microservice communication - no authentication required"""
    queryset = Cirugia2.objects.all()
    serializer_class = Cirugia2Serializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        """Get all surgeries for a specific patient"""
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'patient_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        surgeries = self.queryset.filter(paciente_id=patient_id)
        serializer = self.get_serializer(surgeries, many=True)
        return Response(serializer.data)
