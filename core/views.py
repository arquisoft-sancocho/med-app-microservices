from django.http import JsonResponse

def health_check(request):
    """
    Una vista simple que devuelve un estado 'ok'.
    """
    data = {"status": "ok"}
    return JsonResponse(data)
