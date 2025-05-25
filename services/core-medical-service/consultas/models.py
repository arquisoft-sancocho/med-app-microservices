from django.db import models
from pacientes2.models import Paciente2

class ConsultaMedica(models.Model):
    TIPO_CONSULTA = [
        ('primeravez', 'Primera vez'),
        ('control', 'Control'),
        ('urgente', 'Urgencia'),
        ('prequirurgica', 'Evaluación prequirúrgica'),
        ('postquirurgica', 'Seguimiento postquirúrgico'),
    ]


    nombre = models.CharField(max_length=100)
    paciente = models.ForeignKey(Paciente2, on_delete=models.CASCADE)
    fecha = models.DateTimeField()  # Usar DateTime para registrar hora exacta
    tipo_consulta = models.CharField(max_length=50, choices=TIPO_CONSULTA)
    motivo = models.TextField()
    informacion_extra = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_consulta_display()} - {self.paciente.nombre}"
    
class Prescripcion(models.Model):
    VIA_ADMINISTRACION = [
        ('oral', 'Oral'),
        ('intravenosa', 'Intravenosa'),
        ('intramuscular', 'Intramuscular'),
        ('rectal', 'Rectal'),
        ('sublingual', 'Sublingual'),
    ]

    FRECUENCIA = [
        ('diario', 'Diario'),
        ('12horas', 'Cada 12 horas'),
        ('8horas', 'Cada 8 horas'),
        ('6horas', 'Cada 6 horas'),
        ('prn', 'Cuando sea necesario'),
    ]

    consulta = models.ForeignKey(ConsultaMedica, on_delete=models.CASCADE, related_name='prescripciones')
    medicamento = models.CharField(max_length=100)
    dosis = models.CharField(max_length=100)
    via_administracion = models.CharField(max_length=50, choices=VIA_ADMINISTRACION)
    frecuencia = models.CharField(max_length=50, choices=FRECUENCIA)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.medicamento} - {self.consulta.paciente.nombre}"