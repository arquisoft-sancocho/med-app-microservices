from ..models import Diagnostico

def get_diagnosticos():
    """
    Obtener todos los diagnosticos.
    """
    queryset = Diagnostico.objects.all()
    return (queryset)

def create_diagnostico(form):
    """
    Crea un diagnostico a partir de un form.
    """
    diagnostico = form.save()
    diagnostico.save()
    return diagnostico

def get_diagnostico_by_id(diagnostico_id):
    """
    Obtiene un diagnostico por su ID. Devuelve None si no existe.
    """
    try:
        return Diagnostico.objects.get(id=diagnostico_id)
    except Diagnostico.DoesNotExist:
        return None
    
