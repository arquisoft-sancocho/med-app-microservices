from ..models import ConsultaMedica, Prescripcion

def get_consultas():
    """
    Obtener todas las consultas médicas ordenadas por fecha descendente.
    """
    queryset = ConsultaMedica.objects.all().order_by('-fecha')
    return queryset

def create_consulta(form):
    """
    Crea una consulta médica a partir de un form.
    """
    consulta = form.save()
    consulta.save()
    return consulta

def get_consulta_by_id(consulta_id):
    """
    Obtiene una consulta por su ID. Devuelve None si no existe.
    """
    try:
        return ConsultaMedica.objects.get(id=consulta_id)
    except ConsultaMedica.DoesNotExist:
        return None

def get_prescripciones_by_consulta(consulta_id):
    """
    Obtiene todas las prescripciones asociadas a una consulta.
    """
    try:
        consulta = ConsultaMedica.objects.get(id=consulta_id)
        return consulta.prescripciones.all()
    except ConsultaMedica.DoesNotExist:
        return None

def create_prescripcion(form, consulta_id):
    """
    Crea una prescripción asociada a una consulta.
    """
    try:
        consulta = ConsultaMedica.objects.get(id=consulta_id)
        prescripcion = form.save(commit=False)
        prescripcion.consulta = consulta
        prescripcion.save()
        return prescripcion
    except ConsultaMedica.DoesNotExist:
        return None

def delete_consulta(consulta_id):
    """
    Elimina una consulta y sus prescripciones asociadas.
    Devuelve True si tuvo éxito, False si no encontró la consulta.
    """
    try:
        consulta = ConsultaMedica.objects.get(id=consulta_id)
        consulta.prescripciones.all().delete()
        consulta.delete()
        return True
    except ConsultaMedica.DoesNotExist:
        return False

def get_consultas_by_paciente(paciente_id):
    """
    Obtiene todas las consultas de un paciente específico.
    """
    return ConsultaMedica.objects.filter(paciente__id=paciente_id).order_by('-fecha')

