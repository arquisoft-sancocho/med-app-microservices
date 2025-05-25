from django.db import models

class Cirugia2(models.Model):
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
    paciente_id = models.IntegerField()  # Reference to patient in core service
    tipo = models.CharField(max_length=50, choices=TIPO_CIRUGIA_EPILEPSIA)
    fecha = models.DateField()
    resultado = models.TextField()
    # Campos específicos para epilepsia
    estado_postoperatorio = models.CharField(max_length=50, choices=ESTADO_POSTERIOR)
    complicaciones = models.TextField(blank=True, null=True)
    notas_quirurgicas = models.TextField(blank=True, null=True)

    # Metadata fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Cirugía'
        verbose_name_plural = 'Cirugías'

    def __str__(self):
        return f"{self.get_tipo_display()} - Paciente {self.paciente_id}"

    def get_patient_name(self):
        """
        Get patient name from core service
        This will be implemented as a method that calls the core service
        """
        from django.conf import settings
        import requests

        try:
            response = requests.get(
                f"{settings.CORE_SERVICE_URL}/api/patient/{self.paciente_id}/basic/",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('nombre', f'Paciente {self.paciente_id}')
        except:
            pass
        return f'Paciente {self.paciente_id}'
