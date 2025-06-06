from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import Paciente2Form
from .models import Paciente2
from django.http import HttpResponse
from .logic.paciente2_logic import get_pacientes2, create_paciente2, get_paciente_by_id2, get_historia_clinica, delete_paciente2, get_informacion_critica
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('pacientes2.view_paciente2', raise_exception=True)
def paciente_list2(request):
    pacientes2 = get_pacientes2()
    puede_eliminar = request.user.is_superuser or request.user.groups.filter(name="admin").exists()
    return render(request, 'pacientes2/pacientes2.html', {
        'paciente_list2': pacientes2,
        'puede_eliminar': puede_eliminar
        })


@login_required
def paciente_create2(request):
    if  ( request.user.groups.filter(name__in=["Tecnico"]).exists()):
        messages.error(request, "No tienes permisos para añadir un paciente.")
        return redirect('pacienteList2')

    if request.method == 'POST':
        form = Paciente2Form(request.POST)
        if form.is_valid():
            create_paciente2(form)
            messages.success(request, 'Paciente creado con éxito')
            return redirect('pacienteList2')
    else:
        form = Paciente2Form()

    return render(request, 'pacientes2/pacienteCreate2.html', {'form': form})

@login_required
@permission_required('pacientes2.view_paciente2', raise_exception=True)
def paciente_detail2(request, paciente_id):
    paciente2 = get_paciente_by_id2(paciente_id)
    if not paciente2:
        messages.error(request, "El paciente no existe")
        return redirect('pacienteList2')

    return render(request, 'pacientes2/paciente_detail2.html', {'paciente2': paciente2})

@login_required
@permission_required('pacientes2.view_paciente2', raise_exception=True)
def historia_clinica_view(request, paciente_id):
    historia = get_historia_clinica(paciente_id, request)

    if not historia:
        return HttpResponse("Paciente no encontrado", status=404)

    if  ( request.user.groups.filter(name__in=["Tecnico" ]).exists()):
        historia["cirugias"] = "No tienes permisos para ver esta información."
        historia["consultas"] = "No tienes permisos para ver esta información."

    if  (request.user.groups.filter(name__in=["Enfermero" ]).exists()):
        historia["cirugias"] = "No tienes permisos para ver esta información."

    return render(request, 'pacientes2/historia_clinica.html', historia)

@login_required
@permission_required('pacientes2.delete_paciente2', raise_exception=True)
def paciente_delete2(request, paciente_id):
    if request.method == 'POST':
        success = delete_paciente2(paciente_id)
        if success:
            messages.success(request, 'Paciente eliminado con éxito')
        else:
            messages.error(request, 'No se pudo eliminar el paciente')
        return redirect('pacienteList2')
    else:
        messages.warning(request, 'Método no permitido para eliminar paciente.')
        return redirect('pacienteList2')

@login_required
@permission_required('pacientes2.view_paciente2', raise_exception=True)
def informacion_critica(request, paciente_id):
    informacion = get_informacion_critica(paciente_id, request)

    if not informacion:
        return HttpResponse("Paciente no encontrado", status=404)

    if  ( request.user.groups.filter(name__in=["Tecnico" ]).exists()):
        informacion["cirugias"] = "No tienes permisos para ver esta información."
        informacion["consultas"] = "No tienes permisos para ver esta información."

    if  (request.user.groups.filter(name__in=["Enfermero" ]).exists()):
        informacion["cirugias"] = "No tienes permisos para ver esta información."


    return render(request, 'pacientes2/informacion_critica.html', informacion)

@login_required
def paciente_edit2(request, paciente_id):
    paciente = get_object_or_404(Paciente2, id=paciente_id)

    # Verificar permisos dentro de la vista
    if  (request.user.groups.filter(name__in=["Tecnico"]).exists()):
        messages.error(request, "No tienes permisos para modificar este paciente.")
        return redirect('pacienteDetail2', paciente_id=paciente.id)

    if request.method == 'POST':
        form = Paciente2Form(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente actualizado con éxito.')
            return redirect('pacienteDetail2', paciente_id=paciente.id)
    else:
        form = Paciente2Form(instance=paciente)

    return render(request, 'pacientes2/paciente_edit.html', {
        'form': form,
        'paciente': paciente
    })

