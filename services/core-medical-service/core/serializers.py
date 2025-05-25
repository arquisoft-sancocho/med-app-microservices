"""
Serializers for the core medical service API.
These endpoints will be consumed by other microservices.
"""

from rest_framework import serializers
from pacientes2.models import Paciente2
from consultas.models import ConsultaMedica, Prescripcion


class Paciente2Serializer(serializers.ModelSerializer):
    """Serializer for patient data - used by other microservices"""

    class Meta:
        model = Paciente2
        fields = '__all__'


class Paciente2BasicSerializer(serializers.ModelSerializer):
    """Basic patient info serializer - for lightweight responses"""

    class Meta:
        model = Paciente2
        fields = ['id', 'nombres', 'apellidos', 'cedula', 'fecha_nacimiento', 'genero']


class ConsultaSerializer(serializers.ModelSerializer):
    """Serializer for consultation data"""
    paciente_info = Paciente2BasicSerializer(source='paciente', read_only=True)

    class Meta:
        model = ConsultaMedica
        fields = '__all__'


class PrescripcionSerializer(serializers.ModelSerializer):
    """Serializer for prescription data"""

    class Meta:
        model = Prescripcion
        fields = '__all__'
