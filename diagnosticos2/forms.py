from django import forms
from .models import Diagnostico2, Tratamiento2

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico2
        fields = ['nombre', 'fecha_realizacion', 'paciente', 'resultados_obtenidos', 'info_extra']
        widgets = {
            'fecha_realizacion': forms.DateInput(attrs={'type': 'date'}),
        }

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento2
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'indicaciones']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }