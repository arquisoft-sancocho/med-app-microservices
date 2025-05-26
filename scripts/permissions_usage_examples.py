"""
Django Permissions Usage Examples
=================================

This file contains examples of how to use the permissions and groups
created by the setup-permissions.py script in your Django views.
"""

# BASIC PERMISSION DECORATORS
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView

# =============================================================================
# FUNCTION-BASED VIEW EXAMPLES
# =============================================================================

@login_required
@permission_required('pacientes2.view_paciente2', raise_exception=True)
def patient_list(request):
    """View all patients - requires patient view permission"""
    # Your view logic here
    pass

@login_required
@permission_required('pacientes2.add_paciente2', raise_exception=True)
def patient_create(request):
    """Create new patient - requires patient add permission"""
    # Your view logic here
    pass

@login_required
@permission_required(['examenes2.view_examen2', 'examenes2.add_examen2'], raise_exception=True)
def exam_manage(request):
    """Manage exams - requires multiple permissions"""
    # Your view logic here
    pass

# Custom permission check
@login_required
def patient_detail(request, patient_id):
    """Patient detail with custom permission checks"""

    # Check if user can view patient data
    if not request.user.has_perm('pacientes2.view_paciente2'):
        messages.error(request, "No tienes permisos para ver información de pacientes")
        return redirect('home')

    # Check for emergency access
    if request.user.has_perm('can_access_emergency_data'):
        # Show additional emergency information
        show_emergency_data = True
    else:
        show_emergency_data = False

    # Check if user can view complete medical history
    show_full_history = request.user.has_perm('can_view_patient_history')

    context = {
        'show_emergency_data': show_emergency_data,
        'show_full_history': show_full_history,
    }

    return render(request, 'patients/detail.html', context)

# Group-based access control
@login_required
def medical_dashboard(request):
    """Dashboard that shows different content based on user group"""

    user_groups = request.user.groups.values_list('name', flat=True)

    context = {
        'is_doctor': 'Médicos' in user_groups,
        'is_nurse': 'Enfermeros' in user_groups,
        'is_admin': 'Administradores' in user_groups,
        'is_receptionist': 'Recepcionistas' in user_groups,
        'is_lab_tech': 'Técnicos_Laboratorio' in user_groups,
    }

    return render(request, 'dashboard.html', context)

# =============================================================================
# CLASS-BASED VIEW EXAMPLES
# =============================================================================

class PatientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """List all patients - CBV with permission required"""
    model = Paciente2
    template_name = 'patients/list.html'
    permission_required = 'pacientes2.view_paciente2'

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para ver la lista de pacientes")
        return redirect('home')

class ExamCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create exam - requires specific permission"""
    model = Examen2
    fields = ['paciente', 'tipo_examen', 'descripcion']
    template_name = 'exams/create.html'
    permission_required = 'examenes2.add_examen2'

    def form_valid(self, form):
        # Add the current user as the one who created the exam
        form.instance.created_by = self.request.user
        messages.success(self.request, "Examen creado exitosamente")
        return super().form_valid(form)

class SurgeryApprovalView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Approve surgery - requires surgery approval permission"""
    model = Cirugia
    fields = ['estado', 'notas_aprobacion']
    template_name = 'surgery/approve.html'
    permission_required = 'can_approve_surgeries'

    def dispatch(self, request, *args, **kwargs):
        # Additional check: only doctors can approve surgeries
        if not request.user.groups.filter(name='Médicos').exists():
            messages.error(request, "Solo los médicos pueden aprobar cirugías")
            return redirect('surgery_list')
        return super().dispatch(request, *args, **kwargs)

# =============================================================================
# TEMPLATE USAGE EXAMPLES
# =============================================================================

"""
In your Django templates, you can use the perms template variable:

<!-- Basic permission check -->
{% if perms.pacientes2.add_paciente2 %}
    <a href="{% url 'patient_create' %}" class="btn btn-primary">
        Agregar Paciente
    </a>
{% endif %}

<!-- Multiple permission check -->
{% if perms.examenes2.view_examen2 and perms.examenes2.add_examen2 %}
    <div class="exam-management">
        <!-- Exam management content -->
    </div>
{% endif %}

<!-- Group-based content -->
{% if user.groups.all.0.name == "Médicos" %}
    <div class="doctor-panel">
        <!-- Doctor-specific content -->
    </div>
{% elif user.groups.all.0.name == "Enfermeros" %}
    <div class="nurse-panel">
        <!-- Nurse-specific content -->
    </div>
{% endif %}

<!-- Custom permission check -->
{% if perms.can_view_patient_history %}
    <section class="patient-history">
        <!-- Complete patient history -->
    </section>
{% endif %}

<!-- User info -->
<p>Rol: {{ user.groups.all.0.name|default:"Sin asignar" }}</p>
<p>Permisos: {{ user.get_all_permissions|length }}</p>
"""

# =============================================================================
# MIDDLEWARE EXAMPLE
# =============================================================================

class RoleBasedAccessMiddleware:
    """
    Middleware to control access based on user roles
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Check access before processing view"""

        # Skip for admin and auth views
        if request.path.startswith('/admin/') or request.path.startswith('/accounts/'):
            return None

        # Check if user is authenticated
        if not request.user.is_authenticated:
            return None

        # Role-based URL restrictions
        restricted_paths = {
            '/surgery/': ['Médicos', 'Administradores'],
            '/lab/': ['Técnicos_Laboratorio', 'Médicos', 'Administradores'],
            '/billing/': ['Recepcionistas', 'Administradores'],
            '/audit/': ['Auditores_Médicos', 'Administradores'],
        }

        for path_prefix, allowed_groups in restricted_paths.items():
            if request.path.startswith(path_prefix):
                user_groups = request.user.groups.values_list('name', flat=True)
                if not any(group in allowed_groups for group in user_groups):
                    messages.error(request, f"No tienes acceso a esta sección")
                    return redirect('home')

        return None

# =============================================================================
# CUSTOM PERMISSION CLASSES
# =============================================================================

from django.core.exceptions import PermissionDenied

class MedicalStaffRequired:
    """
    Mixin that requires user to be medical staff (Doctor or Nurse)
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        medical_groups = ['Médicos', 'Enfermeros']
        user_groups = request.user.groups.values_list('name', flat=True)

        if not any(group in medical_groups for group in user_groups):
            raise PermissionDenied("Se requiere ser personal médico")

        return super().dispatch(request, *args, **kwargs)

class DoctorOnlyRequired:
    """
    Mixin that requires user to be a doctor
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.groups.filter(name='Médicos').exists():
            raise PermissionDenied("Se requiere ser médico")

        return super().dispatch(request, *args, **kwargs)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_user_role(user):
    """Get the primary role of a user"""
    groups = user.groups.all()
    if groups:
        return groups[0].name
    return "Sin rol asignado"

def can_access_patient_data(user, patient=None):
    """Check if user can access patient data"""

    # Administrators and doctors have full access
    if user.groups.filter(name__in=['Administradores', 'Médicos']).exists():
        return True

    # Nurses have limited access
    if user.groups.filter(name='Enfermeros').exists():
        return user.has_perm('pacientes2.view_paciente2')

    # Lab technicians can only view basic patient info
    if user.groups.filter(name='Técnicos_Laboratorio').exists():
        return user.has_perm('pacientes2.view_paciente2')

    return False

def get_accessible_sections(user):
    """Get list of sections accessible to user"""

    sections = []
    user_groups = user.groups.values_list('name', flat=True)

    # Basic sections available to all authenticated users
    if user.is_authenticated:
        sections.append('dashboard')

    # Patient management
    if user.has_perm('pacientes2.view_paciente2'):
        sections.append('patients')

    # Exams
    if user.has_perm('examenes2.view_examen2'):
        sections.append('exams')

    # Diagnosis
    if user.has_perm('diagnosticos2.view_diagnostico2'):
        sections.append('diagnosis')

    # Surgery (doctors only)
    if 'Médicos' in user_groups or 'Administradores' in user_groups:
        sections.append('surgery')

    # Lab (lab technicians and medical staff)
    if ('Técnicos_Laboratorio' in user_groups or
        'Médicos' in user_groups or
        'Administradores' in user_groups):
        sections.append('laboratory')

    # Billing (receptionists and admins)
    if ('Recepcionistas' in user_groups or
        'Administradores' in user_groups):
        sections.append('billing')

    # Administration (admins only)
    if 'Administradores' in user_groups:
        sections.append('administration')

    return sections
