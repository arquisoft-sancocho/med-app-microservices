from ..models import Paciente2
from examenes2.models import Examen2
from diagnosticos2.models import Diagnostico2
from cirugias.models import Cirugia
from consultas.models import ConsultaMedica

def get_pacientes2():
    """
    Obtener todos los pacientes.
    """
    queryset = Paciente2.objects.all()
    return (queryset)

def create_paciente2(form):
    """
    Crea un paciente a partir de un form.
    """
    paciente2 = form.save()
    paciente2.save()
    return paciente2

def get_paciente_by_id2(paciente_id):
    """
    Obtiene un paciente por su ID. Devuelve None si no existe.
    """
    try:
        return Paciente2.objects.get(id=paciente_id)
    except Paciente2.DoesNotExist:
        return None
    
def get_historia_clinica(paciente_id):
    """
    Obtiene la historia clínica de un paciente, incluyendo exámenes y diagnósticos.
    """
    paciente = get_paciente_by_id2(paciente_id)
    if not paciente:
        return None
    
    examenes = Examen2.objects.filter(paciente=paciente)
    diagnosticos = Diagnostico2.objects.filter(paciente=paciente)
    cirugias = Cirugia.objects.filter(paciente=paciente)
    consultas = ConsultaMedica.objects.filter(paciente= paciente)
    
    return {
        "paciente": paciente,
        "examenes": examenes,
        "diagnosticos": diagnosticos,
        "cirugias": cirugias,
        "consultas": consultas,
    }
    
def delete_paciente2(paciente_id):
    """
    Elimina un paciente por su ID.
    """
    try:
        paciente = Paciente2.objects.get(id=paciente_id)
        paciente.delete()
        return True
    except Paciente2.DoesNotExist:
        return False
    
