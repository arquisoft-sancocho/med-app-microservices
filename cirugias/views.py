from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import CirugiaForm
from .logic.cirugia_logic import get_cirugia_by_id, get_cirugias, create_cirugia, delete_cirugia

def cirugia_list(request):
    cirugias = get_cirugias()
    return render(request, 'cirugias/cirugias.html', {'cirugia_list': cirugias})

def cirugia_create(request):
    if request.method == 'POST':
        form = CirugiaForm(request.POST)
        if form.is_valid():
            create_cirugia(form)
            messages.success(request, 'Cirugia creado con éxito')
            return redirect('cirugiaList')
    else:
        form = CirugiaForm()
    
    return render(request, 'cirugias/cirugiaCreate.html', {'form': form})

def cirugia_detail(request, cirugia_id):
    cirugia = get_cirugia_by_id(cirugia_id)
    if not cirugia:
        messages.error(request, "El cirugia no existe")
        return redirect('cirugiaList')

    return render(request, 'cirugias/cirugia_detail.html', {'cirugia': cirugia})

def cirugia_delete(request, cirugia_id):
    if request.method == 'POST':
        success = delete_cirugia(cirugia_id)
        if success:
            messages.success(request, 'Cirugia eliminado con éxito')
        else:
            messages.error(request, 'No se pudo eliminar el cirugia')
    return redirect('cirugiaList')
