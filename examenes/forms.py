from django import forms
from .models import Paciente

from django import forms
from .models import Examen

class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['paciente', 'fecha_realizacion', 'tipo_examen', 'resultado']
        widgets = {
            'fecha_realizacion': forms.DateInput(attrs={'type': 'date'}),
        }
