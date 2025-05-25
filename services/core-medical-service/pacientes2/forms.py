from django import forms
from .models import Paciente2

class Paciente2Form(forms.ModelForm):
    class Meta:
        model = Paciente2
        fields = ['nombre', 'edad', 'fecha_nacimiento', 'genero', 'direccion', 'telefono', 'tipo_sangre']
        labels = {
            'nombre': 'Nombre completo',
            'edad': 'Edad',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'genero': 'Género',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'tipo_sangre': 'Tipo de sangre',
        }
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
