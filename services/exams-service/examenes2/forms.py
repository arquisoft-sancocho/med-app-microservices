from django import forms
from .models import Examen2

class Examen2Form(forms.ModelForm):
    class Meta:
        model = Examen2
        fields = ['nombre', 'paciente_id', 'fecha_realizacion', 'tipo_examen', 'resultado']
        labels = {
            'nombre': 'Nombre del Examen',
            'paciente_id': 'Paciente ID',
            'fecha_realizacion': 'Fecha de Realización',
            'tipo_examen': 'Tipo de Examen',
            'resultado': 'Resultado',
        }
        widgets = {
            'fecha_realizacion': forms.DateInput(attrs={'type': 'date'}),
        }
