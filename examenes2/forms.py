from django import forms
from .models import Examen2

class Examen2Form(forms.ModelForm):
    class Meta:
        model = Examen2
        fields = ['nombre', 'paciente', 'fecha_realizacion', 'tipo_examen', 'resultado']
        labels = {
            'nombre': 'Nombre del Examen',
            'paciente': 'Paciente',
            'fecha_realizacion': 'Fecha de Realización',
            'tipo_examen': 'Tipo de Examen',
            'resultado': 'Resultado',
        }
        widgets = {
            'fecha_realizacion': forms.DateInput(attrs={'type': 'date'}),
        }
