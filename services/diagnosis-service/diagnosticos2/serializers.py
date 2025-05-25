from rest_framework import serializers
from .models import Diagnostico2, Tratamiento2

class Tratamiento2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Tratamiento2
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add patient data if available
        patient_data = instance.get_paciente_data()
        if patient_data:
            representation['paciente_data'] = patient_data
        return representation

class Diagnostico2Serializer(serializers.ModelSerializer):
    tratamientos = Tratamiento2Serializer(many=True, read_only=True)

    class Meta:
        model = Diagnostico2
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add patient data if available
        patient_data = instance.get_paciente_data()
        if patient_data:
            representation['paciente_data'] = patient_data
        return representation

class DiagnosticoCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating diagnoses with minimal patient validation"""

    class Meta:
        model = Diagnostico2
        fields = ['nombre', 'fecha_realizacion', 'paciente_id', 'resultados_obtenidos', 'info_extra']

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

class TratamientoCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating treatments with minimal patient validation"""

    class Meta:
        model = Tratamiento2
        fields = ['nombre', 'diagnostico', 'paciente_id', 'fecha_inicio', 'fecha_fin', 'indicaciones']

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
