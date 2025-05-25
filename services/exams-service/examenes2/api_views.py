from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Examen2
from .serializers import Examen2Serializer, ExamenCreateSerializer

class Examen2ViewSet(viewsets.ModelViewSet):
    queryset = Examen2.objects.all()
    serializer_class = Examen2Serializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ExamenCreateSerializer
        return Examen2Serializer

    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        """Get all exams for a specific patient"""
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'patient_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        exams = self.queryset.filter(paciente_id=patient_id)
        serializer = self.get_serializer(exams, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get exams filtered by type"""
        exam_type = request.query_params.get('type')
        if not exam_type:
            return Response(
                {'error': 'type parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        exams = self.queryset.filter(tipo_examen=exam_type)
        serializer = self.get_serializer(exams, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search exams by patient name or exam name"""
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'q parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        exams = self.queryset.filter(
            Q(nombre__icontains=query) |
            Q(paciente_nombre__icontains=query)
        )
        serializer = self.get_serializer(exams, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new exam"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exam = serializer.save()

        # Return full exam data
        response_serializer = Examen2Serializer(exam)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
