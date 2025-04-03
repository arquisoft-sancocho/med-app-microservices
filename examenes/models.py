from django.db import models
from pacientes.models import Paciente

class Examen(models.Model):
    RESULTADOS = [
        ('positivo', 'Positivo'),
        ('negativo', 'Negativo'),
    ]
    
    TIPOS = [
        ('eeg', 'EEG'),
        ( 'rm', 'Resonancia magnética'),
        ( 'mirna', 'MicroRNA')
        ( 'sangre', 'Muestra de sangre'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_realizacion = models.DateField()
    tipo_examen = models.CharField(choices=TIPOS)
    resultado = models.CharField(max_length=10, choices=RESULTADOS)

    def __str__(self):
        return f"{self.tipo_examen} - {self.paciente}"


