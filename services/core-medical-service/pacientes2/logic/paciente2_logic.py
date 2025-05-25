from ..models import Paciente2
import requests
import os
import logging

logger = logging.getLogger(__name__)

# Service URLs from environment variables
EXAMS_SERVICE_URL = os.getenv('EXAMS_SERVICE_URL', 'http://localhost:8001')
DIAGNOSIS_SERVICE_URL = os.getenv('DIAGNOSIS_SERVICE_URL', 'http://localhost:8002')

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

    # Fetch data from microservices
    examenes = []
    diagnosticos = []
    cirugias = []  # These will stay in core service for now
    consultas = []  # These will stay in core service for now

    try:
        # Get exams from exams service
        response = requests.get(f"{EXAMS_SERVICE_URL}/api/examenes/by_patient/?patient_id={paciente_id}")
        if response.status_code == 200:
            examenes = response.json()
    except Exception as e:
        logger.error(f"Error fetching exams for patient {paciente_id}: {e}")

    try:
        # Get diagnostics from diagnosis service
        response = requests.get(f"{DIAGNOSIS_SERVICE_URL}/api/diagnosticos/by_patient/?patient_id={paciente_id}")
        if response.status_code == 200:
            diagnosticos = response.json()
    except Exception as e:
        logger.error(f"Error fetching diagnostics for patient {paciente_id}: {e}")

    return {
        "paciente": paciente,
        "examenes": examenes,
        "diagnosticos": diagnosticos,
        "cirugias": cirugias,
        "consultas": consultas,
    }

def get_informacion_critica(paciente_id):
    """
    Obtiene la información crítica de un paciente.
    """
    paciente = get_paciente_by_id2(paciente_id)
    if not paciente:
        return None

    # Fetch data from microservices
    examenes = []
    diagnosticos = []
    cirugias = []  # These will stay in core service for now
    consultas = []  # These will stay in core service for now

    try:
        # Get exams from exams service
        response = requests.get(f"{EXAMS_SERVICE_URL}/api/examenes/by_patient/?patient_id={paciente_id}")
        if response.status_code == 200:
            examenes = response.json()
    except Exception as e:
        logger.error(f"Error fetching exams for patient {paciente_id}: {e}")

    try:
        # Get diagnostics from diagnosis service
        response = requests.get(f"{DIAGNOSIS_SERVICE_URL}/api/diagnosticos/by_patient/?patient_id={paciente_id}")
        if response.status_code == 200:
            diagnosticos = response.json()
    except Exception as e:
        logger.error(f"Error fetching diagnostics for patient {paciente_id}: {e}")

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

