from django.db import models
import requests
from django.conf import settings

class Diagnostico2(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_realizacion = models.DateField()
    paciente_id = models.IntegerField()  # Reference to patient by ID instead of ForeignKey
    paciente_nombre = models.CharField(max_length=200, blank=True)  # Cache patient name for display
    resultados_obtenidos = models.TextField()
    info_extra = models.TextField()

    class Meta:
        permissions = [
            ("can_make_diagnosis", "Can make diagnosis"),
        ]

    def get_paciente_data(self):
        """Fetch patient data from the core medical service"""
        try:
            core_service_url = getattr(settings, 'CORE_SERVICE_URL', 'http://localhost:8000')
            response = requests.get(f"{core_service_url}/api/pacientes/{self.paciente_id}/")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching patient data: {e}")
        return None

    def save(self, *args, **kwargs):
        # Cache patient name when saving
        if not self.paciente_nombre:
            patient_data = self.get_paciente_data()
            if patient_data:
                self.paciente_nombre = f"{patient_data.get('nombre', '')} {patient_data.get('apellido', '')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre}"

class Tratamiento2(models.Model):
    nombre = models.CharField(max_length=100)
    diagnostico = models.ForeignKey(Diagnostico2, on_delete=models.CASCADE, related_name='tratamientos')
    paciente_id = models.IntegerField()  # Reference to patient by ID instead of ForeignKey
    paciente_nombre = models.CharField(max_length=200, blank=True)  # Cache patient name for display
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    indicaciones = models.TextField()

    def get_paciente_data(self):
        """Fetch patient data from the core medical service"""
        try:
            core_service_url = getattr(settings, 'CORE_SERVICE_URL', 'http://localhost:8000')
            response = requests.get(f"{core_service_url}/api/pacientes/{self.paciente_id}/")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching patient data: {e}")
        return None

    def save(self, *args, **kwargs):
        # Cache patient name when saving
        if not self.paciente_nombre:
            patient_data = self.get_paciente_data()
            if patient_data:
                self.paciente_nombre = f"{patient_data.get('nombre', '')} {patient_data.get('apellido', '')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre}"
