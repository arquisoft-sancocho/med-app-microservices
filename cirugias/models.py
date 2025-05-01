from django.db import models
from pacientes2.models import Paciente2

class Cirugia(models.Model):
    TIPO_CIRUGIA_EPILEPSIA = [
        ('lobectomia', 'Lobectomía Temporal'),
        ('callosotomia', 'Callosotomía Corpus Callosum'),
        ('hemisferectomia', 'Hemisferectomía'),
        ('estimulador', 'Implante de Estimulador VNS'),
        ('resectiva', 'Cirugía Resectiva'),
        ('termocoagulacion', 'Termocoagulación Láser'),
    ]

    ESTADO_POSTERIOR = [
        ('libre', 'Libre de crisis'),
        ('mejoria', 'Mejoría significativa'),
        ('leve', 'Leve mejoría'),
        ('sin_cambios', 'Sin cambios'),
        ('empeoramiento', 'Empeoramiento'),
    ]

    nombre = models.CharField(max_length=100)
    paciente = models.ForeignKey(Paciente2, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=TIPO_CIRUGIA_EPILEPSIA)
    fecha = models.DateField()
    resultado = models.TextField()
    # Campos específicos para epilepsia
    estado_postoperatorio = models.CharField(max_length=50, choices=ESTADO_POSTERIOR)
    complicaciones = models.TextField(blank=True, null=True)
    notas_quirurgicas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.paciente.nombre}"