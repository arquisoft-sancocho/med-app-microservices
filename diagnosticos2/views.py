from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import DiagnosticoForm, TratamientoForm
from .logic.diagnostico_logic import get_diagnosticos, create_diagnostico, get_diagnostico_by_id, delete_diagnostico
from .models import Diagnostico2, Tratamiento2
from django.contrib.auth.decorators import login_required, permission_required
from pacientes2.models import Paciente2

@login_required
def diagnostico_list(request):
    diagnosticos = get_diagnosticos()
    return render(request, 'diagnosticos/diagnosticos.html', {'diagnostico_list': diagnosticos})

@login_required
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

@login_required
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

@login_required
def add_tratamiento(request, diagnostico_id):
    diagnostico = get_object_or_404(Diagnostico2, id=diagnostico_id)

    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            tratamiento = form.save(commit=False)
            tratamiento.diagnostico = diagnostico
            if hasattr(diagnostico, 'paciente'):
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

@login_required
@permission_required('diagnosticos2.delete_diagnostico2', raise_exception=True)
def diagnostico_delete(request, diagnostico_id):
    if request.method == 'POST':
        success = delete_diagnostico(diagnostico_id)
        if success:
            messages.success(request, 'Diagnóstico y tratamientos asociados eliminados con éxito')
        else:
            messages.error(request, 'No se pudo eliminar el diagnóstico')
        return redirect('diagnosticoList')
    else:
        messages.warning(request, 'Método no permitido para eliminar diagnóstico.')
        return redirect('diagnosticoList')

@login_required
@permission_required('diagnosticos2.can_make_diagnosis', raise_exception=True)
def make_diagnosis_view(request, paciente_id):
    paciente = get_object_or_404(Paciente2, pk=paciente_id)
    if request.method == 'POST':
        form = DiagnosticoForm(request.POST)
        if form.is_valid():
            diagnostico = form.save(commit=False)
            diagnostico.paciente = paciente
            diagnostico.save()
            return redirect('pacienteDetail2', paciente_id=paciente.id)
    else:
        form = DiagnosticoForm()
    return render(request, 'diagnosticos2/make_diagnosis.html', {'form': form, 'paciente': paciente})
