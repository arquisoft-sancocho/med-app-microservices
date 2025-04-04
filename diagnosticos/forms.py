from django import forms
from .models import Diagnostico, Tratamiento

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['nombre', 'fecha_realizacion', 'paciente', 'resultados_obtenidos', 'tratamiento', 'info_extra']
        widgets = {
            'fecha_realizacion': forms.DateInput(attrs={'type': 'date'}),
        }

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['nombre', 'paciente', 'fecha_inicio', 'fecha_fin', 'indicaciones']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }
