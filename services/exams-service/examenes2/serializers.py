from rest_framework import serializers
from .models import Examen2

class Examen2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Examen2
        fields = '__all__'

    def create(self, validated_data):
        # When creating an exam, fetch patient data to cache the name
        exam = super().create(validated_data)
        return exam

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add patient data if available
        patient_data = instance.get_paciente_data()
        if patient_data:
            representation['paciente_data'] = patient_data
        return representation

class ExamenCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating exams with minimal patient validation"""

    class Meta:
        model = Examen2
        fields = ['nombre', 'paciente_id', 'fecha_realizacion', 'tipo_examen', 'resultado']

    def validate_paciente_id(self, value):
        """Validate that the patient exists in the core service"""
        from django.conf import settings
        import requests

        try:
            core_service_url = getattr(settings, 'CORE_SERVICE_URL', 'http://localhost:8000')
            response = requests.get(f"{core_service_url}/api/pacientes/{value}/")
            if response.status_code != 200:
                raise serializers.ValidationError(f"Patient with ID {value} not found in core service")
        except requests.exceptions.RequestException:
            # If core service is down, allow creation but log warning
            pass

        return value
