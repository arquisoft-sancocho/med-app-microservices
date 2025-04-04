from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'edad', 'direccion', 'telefono', 'tipo_sangre']
        labels = {
            'nombre': 'Nombre',
            'edad': 'Edad',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'tipo_sangre':'Tipo de sangre',
        }