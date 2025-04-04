from ..models import Examen2

def get_examenes2():
    """
    Obtener todos los examenes.
    """
    queryset = Examen2.objects.all()
    return (queryset)

def create_examen2(form):
    """
    Crea un examen a partir de un form.
    """
    examen2= form.save()
    examen2.save()
    return examen2

def get_examen_by_id2(examen_id2):
    """
    Obtiene un examen por su ID. Devuelve None si no existe.
    """
    try:
        return Examen2.objects.get(id=examen_id2)
    except Examen2.DoesNotExist:
        return None
