from django import forms
from .models import Cirugia

class CirugiaForm(forms.ModelForm):
    class Meta:
        model = Cirugia
        fields = [
            'nombre', 
            'paciente', 
            'tipo', 
            'fecha', 
            'resultado',
            'estado_postoperatorio',
            'complicaciones',
            'notas_quirurgicas'
        ]
        labels = {
            'nombre': 'Nombre de la Cirugía',
            'paciente': 'Paciente',
            'tipo': 'Tipo de Cirugía',
            'fecha': 'Fecha de la Cirugía',
            'resultado': 'Resultado',
            'estado_postoperatorio': 'Estado Postoperatorio',
            'complicaciones': 'Complicaciones',
            'notas_quirurgicas': 'Notas Quirúrgicas'
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'resultado': forms.Textarea(attrs={'rows': 3}),
            'complicaciones': forms.Textarea(attrs={'rows': 3}),
            'notas_quirurgicas': forms.Textarea(attrs={'rows': 3}),
        }