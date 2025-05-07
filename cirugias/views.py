from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import CirugiaForm
from .models import Cirugia
from .logic.cirugia_logic import get_cirugia_by_id, get_cirugias, create_cirugia, delete_cirugia
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def cirugia_list(request):
    cirugias = get_cirugias()
    puede_eliminar = request.user.is_superuser or request.user.groups.filter(name="Administrador").exists()
    return render(request, 'cirugias/cirugias.html', {
        'cirugia_list': cirugias,
        'puede_eliminar': puede_eliminar                                         
        })


@login_required
# @permission_required('cirugias.add_cirugia', raise_exception=True)
def cirugia_create(request):
    
    if ( request.user.groups.filter(name__in=["Tecnico", "Enfermero"]).exists()):
        messages.error(request, "No tienes permisos para añadir una cirugía.")
        return redirect('cirugiaList')
    
    if request.method == 'POST':
        form = CirugiaForm(request.POST)
        if form.is_valid():
            create_cirugia(form)
            messages.success(request, 'Cirugia creado con éxito')
            return redirect('cirugiaList')
    else:
        form = CirugiaForm()

    return render(request, 'cirugias/cirugiaCreate.html', {'form': form})

@login_required
def cirugia_detail(request, cirugia_id):
    cirugia = get_cirugia_by_id(cirugia_id)
    if not cirugia:
        messages.error(request, "La cirugia no existe")
        return redirect('cirugiaList')

    return render(request, 'cirugias/cirugia_detail.html', {'cirugia': cirugia})

@login_required
@permission_required('cirugias.delete_cirugia', raise_exception=True)
def cirugia_delete(request, cirugia_id):
    if request.method == 'POST':
        success = delete_cirugia(cirugia_id)
        if success:
            messages.success(request, 'Cirugia eliminado con éxito')
        else:
            messages.error(request, 'No se pudo eliminar el cirugia')
        return redirect('cirugiaList')
    else:
        messages.warning(request, 'Método no permitido para eliminar cirugía.')
        return redirect('cirugiaList')
    
    
@login_required
def cirugia_edit(request, cirugia_id):
    cirugia = get_object_or_404(Cirugia, id=cirugia_id)

    # Verificar permisos dentro de la vista
    if  (request.user.groups.filter(name__in=["Tecnico", "Enfermero"]).exists()):
        messages.error(request, "No tienes permisos para modificar esta cirugía.")
        return redirect('cirugiaDetail', cirugia_id=cirugia_id)

    if request.method == 'POST':
        form = CirugiaForm(request.POST, instance=cirugia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cirugía actualizada con éxito.')
            return redirect('cirugiaDetail', cirugia_id=cirugia.id)
    else:
        form = CirugiaForm(instance=cirugia)

    return render(request, 'cirugias/cirugia_edit.html', {
        'form': form,
        'cirugia': cirugia
    })

