from django.db import models
from pacientes2.models import Paciente2

class Examen2(models.Model):
    RESULTADOS = [
        ('positivo', 'Positivo'),
        ('negativo', 'Negativo'),
    ]
    
    TIPOS = [
        ('eeg', 'EEG'),
        ( 'rm', 'Resonancia magnética'),
        ( 'mirna', 'MicroRNA'),
        ( 'sangre', 'Muestra de sangre'),
    ]

    nombre = models.CharField(max_length=100)
    paciente = models.ForeignKey(Paciente2, on_delete=models.CASCADE)
    fecha_realizacion = models.DateField()
    tipo_examen = models.CharField(max_length=10, choices=TIPOS)
    resultado = models.CharField(max_length=35, choices=RESULTADOS)

    def __str__(self):
        return f"{self.tipo_examen} - {self.paciente}"


