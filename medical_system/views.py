from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    grupos_restringidos = ['Tecnico', 'Enfermero']
    tiene_permiso_extra = not request.user.groups.filter(name__in=grupos_restringidos).exists()
    tiene_permiso_unico = not request.user.groups.filter(name__in= ["Tecnico"]).exists()
    return render(request, 'index.html', {'tiene_permiso_extra': tiene_permiso_extra}, {'tiene_permiso_unico': tiene_permiso_unico})

