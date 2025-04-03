from ..models import Examen

def get_examenes():
    """
    Obtener todos los examenes.
    """
    queryset = Examen.objects.all()
    return (queryset)

def create_examen(form):
    """
    Crea un examen a partir de un form.
    """
    examen = form.save()
    examen.save()
    return examen

def get_examen_by_id(examen_id):
    """
    Obtiene un examen por su ID. Devuelve None si no existe.
    """
    try:
        return Examen.objects.get(id=examen_id)
    except Examen.DoesNotExist:
        return None
