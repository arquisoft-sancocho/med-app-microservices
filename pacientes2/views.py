from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import Paciente2Form
from django.http import HttpResponse
from .logic.paciente2_logic import get_pacientes2, create_paciente2, get_paciente_by_id2, get_historia_clinica, delete_paciente2, get_informacion_critica

def paciente_list2(request):
    pacientes2 = get_pacientes2()
    return render(request, 'pacientes2/pacientes2.html', {'paciente_list2': pacientes2})

def paciente_create2(request):
    if request.method == 'POST':
        form = Paciente2Form(request.POST)
        if form.is_valid():
            create_paciente2(form)
            messages.success(request, 'Paciente creado con éxito')
            return redirect('pacienteList2')
    else:
        form = Paciente2Form()
    
    return render(request, 'pacientes2/pacienteCreate2.html', {'form': form})

def paciente_detail2(request, paciente_id):
    paciente2 = get_paciente_by_id2(paciente_id)
    if not paciente2:
        messages.error(request, "El paciente no existe")
        return redirect('pacienteList2')

    return render(request, 'pacientes2/paciente_detail2.html', {'paciente2': paciente2})


def historia_clinica_view(request, paciente_id):
    historia = get_historia_clinica(paciente_id)

    if not historia:
        return HttpResponse("Paciente no encontrado", status=404)

    return render(request, 'pacientes2/historia_clinica.html', historia)

def paciente_delete2(request, paciente_id):
    if request.method == 'POST':
        success = delete_paciente2(paciente_id)
        if success:
            messages.success(request, 'Paciente eliminado con éxito')
        else:
            messages.error(request, 'No se pudo eliminar el paciente')
    return redirect('pacienteList2')

def informacion_critica(request, paciente_id):
    informacion = get_informacion_critica(paciente_id)

    if not informacion:
        return HttpResponse("Paciente no encontrado", status=404)

    return render(request, 'pacientes2/informacion_critica.html', informacion)
