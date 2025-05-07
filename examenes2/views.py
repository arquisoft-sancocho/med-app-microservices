from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import Examen2Form
from .models import Examen2
from .logic.examen2_logic import get_examenes2, create_examen2, get_examen_by_id2, delete_examen2
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def examen_list2(request):
    examenes = get_examenes2()
    puede_eliminar = request.user.is_superuser or request.user.groups.filter(name="admin").exists()
    return render(request, 'examenes2/examenes2.html', {
        'examen_list2': examenes,
        'puede_eliminar': puede_eliminar
        })

    
@login_required
# @permission_required('examenes2.add_examen2', raise_exception=True) # Add if needed
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

@login_required
def examen_detail2(request, examen_id):
    examen2 = get_examen_by_id2(examen_id)
    if not examen2:
        messages.error(request, "El examen no existe")
        return redirect('examenList2')

    return render(request, 'examenes2/examen_detail2.html', {'examen2': examen2})

@login_required
@permission_required('examenes2.delete_examen2', raise_exception=True)
def examen_delete2(request, examen_id):
    # Ensure only POST requests are allowed for deletion
    if request.method == 'POST':
        success = delete_examen2(examen_id)
        if success:
            messages.success(request, 'Examen eliminado con éxito')
        else:
            messages.error(request, 'No se pudo eliminar el examen')
        return redirect('examenList2')
    else:
        # Redirect GET requests away
        messages.warning(request, 'Método no permitido para eliminar examen.')
        return redirect('examenList2')
    
@login_required
def examen_edit2(request, examen_id):
    examen = get_object_or_404(Examen2, id=examen_id)

    if request.method == 'POST':
        form = Examen2Form(request.POST, instance=examen)
        if form.is_valid():
            form.save()
            messages.success(request, 'Examen actualizado con éxito.')
            return redirect('examenDetail2', examen_id=examen.id)
    else:
        form = Examen2Form(instance=examen)

    return render(request, 'examenes2/examen_edit2.html', {
        'form': form,
        'examen': examen
    })

