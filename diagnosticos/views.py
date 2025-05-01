from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import DiagnosticoForm, TratamientoForm
from .logic.diagnostico_logic import get_diagnosticos, create_diagnostico, get_diagnostico_by_id
from .models import Diagnostico, Tratamiento

def diagnostico_list(request):
    diagnosticos = get_diagnosticos()
    return render(request, 'diagnosticos/diagnosticos.html', {'diagnostico_list': diagnosticos})

def diagnostico_create(request):
    if request.method == 'POST':
        form = DiagnosticoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Diagnóstico creado con éxito')
            return redirect('diagnosticoList')
    else:
        form = DiagnosticoForm()
    
    return render(request, 'diagnosticos/diagnosticoCreate.html', {'form': form})

def diagnostico_detail(request, diagnostico_id):
    diagnostico = get_diagnostico_by_id(diagnostico_id)
    if not diagnostico:
        messages.error(request, "El diagnóstico no existe")
        return redirect('diagnosticoList')
    
    tratamientos = diagnostico.tratamientos.all()
    
    return render(request, 'diagnosticos/diagnostico_detail.html', {
        'diagnostico': diagnostico,
        'tratamientos': tratamientos
    })

def add_tratamiento(request, diagnostico_id):
    diagnostico = get_object_or_404(Diagnostico, id=diagnostico_id)
    
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            tratamiento = form.save(commit=False)
            tratamiento.diagnostico = diagnostico
            tratamiento.paciente = diagnostico.paciente
            tratamiento.save()
            messages.success(request, 'Tratamiento añadido con éxito')
            return redirect('diagnosticoDetail', diagnostico_id=diagnostico.id)
    else:
        form = TratamientoForm()
    
    return render(request, 'diagnosticos/add_tratamiento.html', {
        'form': form,
        'diagnostico': diagnostico
    })