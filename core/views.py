import logging
from django.http import HttpResponse, JsonResponse
from django.db import connection, OperationalError

logger = logging.getLogger(_name_)

def readiness_check(request):
    db_ready = False
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_ready = True
    except Exception as e:
        logger.error(f"Readiness probe - DB connection error: {e}")
        db_ready = False

    is_ready = db_ready

    if is_ready:
        return HttpResponse("Ready", status=200, content_type="text/plain")
    else:
        return HttpResponse("Unavailable", status=503, content_type="text/plain")

def liveness_check(request):
    return HttpResponse("Alive", status=200, content_type="text/plain")
