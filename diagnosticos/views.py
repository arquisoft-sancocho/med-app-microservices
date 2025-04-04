from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import DiagnosticoForm, TratamientoForm
from .logic.diagnostico_logic import get_diagnosticos, create_diagnostico, get_diagnostico_by_id
from .models import Diagnostico, Tratamiento

def diagnostico_list(request):
    diagnosticos = get_diagnosticos()
    return render(request, 'diagnosticos/diagnosticos.html', {'diagnostico_list': diagnosticos})

def diagnostico_create(request):
    if request.method == 'POST':
        form = DiagnosticoForm(request.POST)
        tratamiento_form = TratamientoForm(request.POST) if 'tratamiento_aplica' in request.POST else None


            # Si se selecciona tratamiento y el formulario es válido, guardarlo
        if form.is_valid() and (tratamiento_form is None or tratamiento_form.is_valid()):
                diagnostico = form.save(commit=False)
                if tratamiento_form:
                    tratamiento = tratamiento_form.save()
                    diagnostico.tratamiento = tratamiento
                diagnostico.save()
                return redirect('diagnosticoList')

    else:
        form = DiagnosticoForm()
        tratamiento_form = TratamientoForm()

    return render(request, 'diagnosticos/diagnosticoCreate.html', {
        'form': form,
        'tratamiento_form': tratamiento_form
    })

def diagnostico_detail(request, diagnostico_id):
    diagnostico = get_diagnostico_by_id(diagnostico_id)
    if not diagnostico:
        messages.error(request, "El diagnóstico no existe")
        return redirect('diagnosticoList')

    return render(request, 'diagnosticos/diagnostico_detail.html', {'diagnostico': diagnostico})

def diagnostico_update(request, diagnostico_id):
    diagnostico = get_object_or_404(Diagnostico, id=diagnostico_id)
    tratamiento = Tratamiento.objects.filter(paciente=diagnostico.paciente).first()

    if request.method == 'POST':
        form = DiagnosticoForm(request.POST, instance=diagnostico)
        tratamiento_form = TratamientoForm(request.POST, instance=tratamiento) if 'tratamiento_aplica' in request.POST else None

        if form.is_valid():
            form.save()
            
            if tratamiento_form and tratamiento_form.is_valid():
                tratamiento = tratamiento_form.save(commit=False)
                tratamiento.paciente = diagnostico.paciente
                tratamiento.save()
            elif tratamiento:
                # Si se deseleccionó tratamiento, eliminarlo
                tratamiento.delete()

            messages.success(request, "Diagnóstico actualizado con éxito")
            return redirect('diagnosticoList')

    else:
        form = DiagnosticoForm(instance=diagnostico)
        tratamiento_form = TratamientoForm(instance=tratamiento)

    return render(request, 'diagnosticos/diagnosticoUpdate.html', {
        'form': form,
        'tratamiento_form': tratamiento_form
    })
