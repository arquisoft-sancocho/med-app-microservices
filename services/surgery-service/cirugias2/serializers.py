from rest_framework import serializers
from .models import Cirugia2
from django.conf import settings
import requests

class Cirugia2Serializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = Cirugia2
        fields = '__all__'

    def get_patient_name(self, obj):
        """Get patient name from core service"""
        try:
            response = requests.get(
                f"{settings.CORE_SERVICE_URL}/api/patient/{obj.paciente_id}/basic/",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('nombre', f'Paciente {obj.paciente_id}')
        except:
            pass
        return f'Paciente {obj.paciente_id}'

    def validate_paciente_id(self, value):
        """Validate that patient exists in core service"""
        try:
            response = requests.get(
                f"{settings.CORE_SERVICE_URL}/api/patient/{value}/basic/",
                timeout=5
            )
            if response.status_code != 200:
                raise serializers.ValidationError('Patient not found')
        except requests.RequestException:
            raise serializers.ValidationError('Error validating patient')
        return value


class Cirugia2BasicSerializer(serializers.ModelSerializer):
    """Basic serializer for surgery data without patient validation"""

    class Meta:
        model = Cirugia2
        fields = ['id', 'nombre', 'paciente_id', 'tipo', 'fecha', 'estado_postoperatorio']
