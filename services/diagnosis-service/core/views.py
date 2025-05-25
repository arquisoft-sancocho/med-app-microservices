from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET"])
@csrf_exempt
def readiness_check(request):
    """
    Readiness check for the diagnosis service
    """
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({
            'status': 'ready',
            'service': 'diagnosis-service',
            'database': 'connected'
        })
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return JsonResponse({
            'status': 'not ready',
            'service': 'diagnosis-service',
            'error': str(e)
        }, status=503)

@require_http_methods(["GET"])
@csrf_exempt
def liveness_check(request):
    """
    Liveness check for the diagnosis service
    """
    return JsonResponse({
        'status': 'alive',
        'service': 'diagnosis-service'
    })
