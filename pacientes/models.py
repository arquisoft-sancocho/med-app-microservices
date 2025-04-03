from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    tipo_sangre = models.CharField(max_length=3, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.nombre} ({self.edad} años)"


