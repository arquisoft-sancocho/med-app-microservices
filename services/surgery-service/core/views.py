from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

@require_http_methods(["GET"])
@csrf_exempt
def readiness_check(request):
    """
    Readiness check for the surgery service
    """
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({
            'status': 'ready',
            'service': 'surgery-service',
            'database': 'connected'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'not ready',
            'service': 'surgery-service',
            'error': str(e)
        }, status=503)

@require_http_methods(["GET"])
@csrf_exempt
def liveness_check(request):
    """
    Liveness check for the surgery service
    """
    return JsonResponse({
        'status': 'alive',
        'service': 'surgery-service'
    })
