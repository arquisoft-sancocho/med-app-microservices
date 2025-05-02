from django import forms
from .models import ConsultaMedica, Prescripcion

class ConsultaMedicaForm(forms.ModelForm):
    class Meta:
        model = ConsultaMedica
        fields = [
            'nombre',
            'paciente',
            'fecha',
            'tipo_consulta',
            'motivo',
            'informacion_extra'
        ]
        widgets = {
            'fecha': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'motivo': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            }),
            'informacion_extra': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            }),
        }
        labels = {
            'nombre': 'Nombre de la Consulta',
            'tipo_consulta': 'Tipo de Consulta',
            'informacion_extra': 'Información Adicional'
        }

class PrescripcionForm(forms.ModelForm):
    class Meta:
        model = Prescripcion
        fields = [
            'medicamento',
            'dosis',
            'via_administracion',
            'frecuencia',
            'fecha_inicio',
            'fecha_fin'
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del medicamento'
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500mg'
            }),
        }
        labels = {
            'via_administracion': 'Vía de Administración',
            'frecuencia': 'Frecuencia de Dosificación'
        }