# medical_system/context_processors.py

def permisos_usuario(request):
    grupos_restringidos = ['Tecnico', 'Enfermero']
    tiene_permiso_extra = not request.user.groups.filter(name__in=grupos_restringidos).exists() if request.user.is_authenticated else False
    tiene_permiso_unico = not request.user.groups.filter(name__in=["Tecnico"]).exists() if request.user.is_authenticated else False
    return {'tiene_permiso_extra': tiene_permiso_extra, 'tiene_permiso_unico': tiene_permiso_unico }
