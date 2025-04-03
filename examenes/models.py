from django.db import models
from pacientes.models import Paciente

class TipoExamen(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Examen(models.Model):
    RESULTADOS = [
        ('positivo', 'Positivo'),
        ('negativo', 'Negativo'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_realizacion = models.DateField()
    tipo_examen = models.ForeignKey(TipoExamen, on_delete=models.CASCADE)
    resultado = models.CharField(max_length=10, choices=RESULTADOS)

    def __str__(self):
        return f"{self.tipo_examen} - {self.paciente}"


