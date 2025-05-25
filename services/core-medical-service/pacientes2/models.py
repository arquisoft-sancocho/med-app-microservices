from django.db import models

class Paciente2(models.Model):
    GENERO = [
        ('femenino', 'Femenino'),
        ('masculino', 'Masculino'),
        ('otro', 'Otro'),
    ]
    
    SANGRE = [
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
    ]
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=15, choices=GENERO)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    tipo_sangre = models.CharField(max_length=5, choices=SANGRE)
    fecha_registro = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.nombre} ({self.edad} años)"


