from django.db import models
from pacientes2.models import Paciente2

class Diagnostico(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_realizacion = models.DateField()
    paciente = models.ForeignKey(Paciente2, on_delete=models.CASCADE)
    resultados_obtenidos = models.TextField()
    info_extra = models.TextField()

    def __str__(self):
        return f"{self.nombre}"

class Tratamiento(models.Model):
    nombre = models.CharField(max_length=100)
    diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE, related_name='tratamientos')
    paciente = models.ForeignKey(Paciente2, on_delete=models.CASCADE) 
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    indicaciones = models.TextField()

    def __str__(self):
        return f"{self.nombre}"