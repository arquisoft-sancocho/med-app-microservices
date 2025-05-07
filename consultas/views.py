from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ConsultaMedicaForm, PrescripcionForm
from .logic.consulta_logic import get_consulta_by_id, get_consultas, delete_consulta
from .models import ConsultaMedica, Prescripcion
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView, DetailView
from django.urls import reverse_lazy

@login_required
def consulta_list(request):
    consultas = get_consultas()
    puede_eliminar = request.user.is_superuser or request.user.groups.filter(name="admin").exists()
    return render(request, 'consultas/consultas.html', {
        'consulta_list': consultas,
        'puede_eliminar': puede_eliminar
        })

@login_required
def consulta_create(request):
    
     # Verificar permisos: cualquiera puede añadir una consulta menos los médicos
    if not (request.user.is_superuser or request.user.groups.filter(name__in=["admin", "Medico Junta Medica", "Medico", "Enfermero"]).exists()):
        messages.error(request, "No tienes permisos para añadir una consulta.")
        return redirect('consultaList')
    
    if request.method == 'POST':
        form = ConsultaMedicaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta creada con éxito')
            return redirect('consultaList')
    else:
        form = ConsultaMedicaForm()

    return render(request, 'consultas/consultaCreate.html', {'form': form})

@login_required
def consulta_detail(request, consulta_id):
    consulta = get_consulta_by_id(consulta_id)
    if not consulta:
        messages.error(request, "La consulta no existe")
        return redirect('consultaList')

    prescripciones = consulta.prescripciones.all()

    return render(request, 'consultas/consulta_detail.html', {
        'consulta': consulta,
        'prescripciones': prescripciones
    })

@login_required
def add_prescripcion(request, consulta_id):
    
    if not (request.user.is_superuser or request.user.groups.filter(name__in=["admin", "Medico Junta Medica", "Medico", "Enfermero"]).exists()):
        messages.error(request, "No tienes permisos para añadir una prescripción.")
        return redirect('consultaDetail', consulta_id=consulta_id)
    
    consulta = get_object_or_404(ConsultaMedica, id=consulta_id)

    if request.method == 'POST':
        form = PrescripcionForm(request.POST)
        if form.is_valid():
            prescripcion = form.save(commit=False)
            prescripcion.consulta = consulta
            prescripcion.paciente = consulta.paciente
            prescripcion.save()
            messages.success(request, 'prescripcion añadido con éxito')
            return redirect('consultaDetail', consulta_id=consulta.id)
    else:
        form = PrescripcionForm()

    return render(request, 'consultas/add_prescripcion.html', {
        'form': form,
        'consulta': consulta
    })

@login_required
#@permission_required('consultas.delete_consultamedica', raise_exception=True)
def consulta_delete(request, consulta_id):
    if request.method == 'POST':
        success = delete_consulta(consulta_id)
        if success:
            messages.success(request, 'Consulta y prescripciones asociadas eliminados con éxito')
        else:
            messages.error(request, 'No se pudo eliminar la consulta')
        return redirect('consultaList')
    else:
        messages.warning(request, 'Método no permitido para eliminar consulta.')
        return redirect('consultaList')

class ConsultaMedicaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ConsultaMedica
    form_class = ConsultaMedicaForm
    template_name = 'consultas/consulta_edit.html'
    permission_required = 'consultas.change_consultamedica'
    pk_url_kwarg = 'consulta_id'

    def get_success_url(self):
        return reverse_lazy('consultaDetail', kwargs={'consulta_id': self.object.pk})
    
@login_required
def consulta_edit(request, consulta_id):
    consulta = get_object_or_404(ConsultaMedica, id=consulta_id)

    # Verificar permisos dentro de la vista
    if not (request.user.is_superuser or request.user.groups.filter(name__in=["admin", "Medico Junta Medica", "Medico", "Enfermero"]).exists()):
        messages.error(request, "No tienes permisos para modificar esta consulta.")
        return redirect('consultaDetail', consulta_id=consulta_id)

    if request.method == 'POST':
        form = ConsultaMedicaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta actualizada con éxito.')
            return redirect('consultaDetail', consulta_id=consulta.id)
    else:
        form = ConsultaMedicaForm(instance=consulta)

    return render(request, 'consultas/consulta_edit.html', {
        'form': form,
        'consulta': consulta
    })

