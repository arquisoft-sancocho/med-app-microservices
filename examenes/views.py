from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import ExamenForm
from .logic.examen_logic import get_examenes, create_examen, get_examen_by_id

def examen_list(request):
    examenes = get_examenes()
    return render(request, 'examenes/examenes.html', {'examen_list': examenes})

def examen_create(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)
        if form.is_valid():
            create_examen(form)
            messages.success(request, 'Examen creado con éxito')
            return redirect('examenList')
    else:
        form = ExamenForm()
    
    return render(request, 'examenes/examenCreate.html', {'form': form})

def examen_detail(request, examen_id):
    examen = get_examen_by_id(examen_id)
    if not examen:
        messages.error(request, "El examen no existe")
        return redirect('examenList')

    return render(request, 'examenes/examen_detail.html', {'examen': examen})
