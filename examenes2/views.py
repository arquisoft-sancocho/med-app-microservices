from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import Examen2Form
from .logic.examen2_logic import get_examenes2, create_examen2, get_examen_by_id2

def examen_list2(request):
    examenes = get_examenes2()
    return render(request, 'examenes2/examenes2.html', {'examen_list2': examenes})

def examen_create2(request):
    if request.method == 'POST':
        form = Examen2Form(request.POST)
        if form.is_valid():
            create_examen2(form)
            messages.success(request, 'Examen creado con éxito')
            return redirect('examenList2')
    else:
        form = Examen2Form()
    
    return render(request, 'examenes2/examenCreate2.html', {'form': form})

def examen_detail2(request, examen_id):
    examen2 = get_examen_by_id2(examen_id)
    if not examen2:
        messages.error(request, "El examen no existe")
        return redirect('examenList2')

    return render(request, 'examenes2/examen_detail2.html', {'examen2': examen2})
