from ..models import Paciente2
from core.microservice_client import microservice_client
from consultas.models import ConsultaMedica
import logging

logger = logging.getLogger(__name__)

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

def get_historia_clinica(paciente_id, request=None):
    """
    Obtiene la historia clínica de un paciente, incluyendo exámenes y diagnósticos.
    """
    paciente = get_paciente_by_id2(paciente_id)
    if not paciente:
        return None

    # Fetch data from microservices using the client
    examenes = microservice_client.get_patient_exams(paciente_id, request)
    diagnosticos = microservice_client.get_patient_diagnoses(paciente_id, request)
    cirugias = microservice_client.get_patient_surgeries(paciente_id, request)

    # Get consultations from local database
    consultas = list(ConsultaMedica.objects.filter(paciente_id=paciente_id).values(
        'id', 'fecha', 'motivo_consulta', 'diagnostico_principal',
        'plan_tratamiento', 'observaciones'
    ))

    return {
        "paciente": paciente,
        "examenes": examenes,
        "diagnosticos": diagnosticos,
        "cirugias": cirugias,
        "consultas": consultas,
    }

def get_informacion_critica(paciente_id, request=None):
    """
    Obtiene la información crítica de un paciente.
    """
    paciente = get_paciente_by_id2(paciente_id)
    if not paciente:
        return None

    # Fetch data from microservices using the client
    examenes = microservice_client.get_patient_exams(paciente_id, request)
    diagnosticos = microservice_client.get_patient_diagnoses(paciente_id, request)
    cirugias = microservice_client.get_patient_surgeries(paciente_id, request)

    # Get consultations from local database
    consultas = list(ConsultaMedica.objects.filter(paciente_id=paciente_id).values(
        'id', 'fecha', 'motivo_consulta', 'diagnostico_principal',
        'plan_tratamiento', 'observaciones'
    ))

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

