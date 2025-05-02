import logging
from django.http import HttpResponse # JsonResponse no se usa, se puede quitar si quieres
from django.db import connection, OperationalError

# --- CORREGIDO: Usar doble guion bajo para _name_ ---
logger = logging.getLogger(__name__)

# --- MANTENIDO: Funciones para las sondas ---
def readiness_check(request):
    """
    /health/ready: Usada por Startup Probe. Verifica conexión a BD.
    """
    db_ready = False
    try:
        # Intenta una consulta simple a la BD
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_ready = True
        logger.info("Startup/Readiness probe: Database connection successful.") # Log de éxito
    except Exception as e:
        # Loguea el error si la conexión falla
        logger.error(f"Startup/Readiness probe - DB connection error: {e}")
        db_ready = False

    # is_ready será True solo si db_ready es True
    is_ready = db_ready

    if is_ready:
        # Devuelve 200 OK si la BD está lista
        return HttpResponse("Ready", status=200, content_type="text/plain")
    else:
        # Devuelve 503 si la BD no está lista (o hubo otro error)
        return HttpResponse("Unavailable", status=503, content_type="text/plain")

def liveness_check(request):
    """
    /health/live: Usada por Liveness Probe. Verifica que el proceso responde.
    """
    # Simplemente devuelve 200 OK para indicar que el proceso está vivo.
    logger.debug("Liveness probe successful.") # Log opcional
    return HttpResponse("Alive", status=200, content_type="text/plain")