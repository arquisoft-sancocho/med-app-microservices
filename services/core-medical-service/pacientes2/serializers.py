from rest_framework import serializers
from .models import Paciente2

class Paciente2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente2
        fields = '__all__'

class Paciente2BasicSerializer(serializers.ModelSerializer):
    """Serializer básico para datos mínimos de paciente"""
    class Meta:
        model = Paciente2
        fields = ['id', 'nombre', 'edad', 'genero', 'fecha_nacimiento']
