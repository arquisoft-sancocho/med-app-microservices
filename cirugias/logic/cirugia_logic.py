from ..models import Cirugia

def get_cirugias():
    """
    Obtener todas los cirugias.
    """
    queryset = Cirugia.objects.all()
    return (queryset)

def create_cirugia(form):
    """
    Crea un cirugia a partir de un form.
    """
    cirugia= form.save()
    cirugia.save()
    return cirugia

def get_cirugia_by_id(cirugia_id):
    """
    Obtiene un cirugia por su ID. Devuelve None si no existe.
    """
    try:
        return Cirugia.objects.get(id=cirugia_id)
    except Cirugia.DoesNotExist:
        return None
    
def delete_cirugia(cirugia_id):
    """
    Elimina un cirugia por su ID.
    """
    try:
        cirugia = Cirugia.objects.get(id=cirugia_id)
        cirugia.delete()
        return True
    except Cirugia.DoesNotExist:
        return False
