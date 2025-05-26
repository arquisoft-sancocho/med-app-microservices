# Sistema de Permisos - Aplicacion Medica

## Resumen

Este documento describe el sistema de permisos implementado para la aplicacion medica. El sistema define grupos de usuarios con permisos especificos para diferentes funcionalidades del sistema.

## Grupos de Usuarios

### 1. Administradores
**Responsabilidades**: Gestion completa del sistema
**Permisos**:
- Gestion de usuarios (crear, modificar, eliminar, ver)
- Gestion de grupos y permisos
- Acceso al panel de administracion
- Configuracion del sistema
- Ver todos los reportes

### 2. Medicos
**Responsabilidades**: Atencion medica y tratamientos
**Permisos**:
- Ver historial medico de pacientes
- Crear prescripciones medicas
- Aprobar cirugias
- Ver registros medicos
- Actualizar estado de pacientes
- Programar cirugias
- Acceder a resultados de laboratorio
- Modificar tratamientos

### 3. Enfermeros
**Responsabilidades**: Cuidado directo de pacientes
**Permisos**:
- Actualizar signos vitales
- Administrar medicamentos
- Ver horarios de pacientes
- Actualizar notas de pacientes
- Asistir en procedimientos
- Acceder a registros de pacientes

### 4. Recepcionistas
**Responsabilidades**: Atencion al publico y administracion
**Permisos**:
- Programar citas
- Gestionar informacion de pacientes
- Manejar facturacion
- Generar reportes
- Ver horarios
- Actualizar informacion de contacto

### 5. Tecnicos_Laboratorio
**Responsabilidades**: Laboratorio clinico
**Permisos**:
- Procesar muestras de laboratorio
- Actualizar resultados de laboratorio
- Gestionar equipos
- Generar reportes de laboratorio
- Control de calidad

### 6. Auditores_Medicos
**Responsabilidades**: Auditoria y cumplimiento
**Permisos**:
- Revisar registros medicos
- Auditar procedimientos
- Generar reportes de auditoria
- Acceder a datos de cumplimiento
- Revisar facturacion

### 7. Farmaceuticos
**Responsabilidades**: Farmacia y medicamentos
**Permisos**:
- Dispensar medicamentos
- Gestionar inventario
- Verificar prescripciones
- Asesorar pacientes
- Rastrear uso de medicamentos

## Instalacion

### Opcion 1: Usando Django Management Command

```bash
# Desde el directorio del proyecto Django
cd /path/to/core-medical-service
python manage.py setup_permissions
```

### Opcion 2: Usando Cloud Run Job

```bash
# Ejecutar en Cloud Run (recomendado para produccion)
cd /path/to/scripts
./setup_permissions_cloud_run.sh
```

### Opcion 3: Usando SQL Directo

```bash
# Conectar a la base de datos y ejecutar
psql -d medical_system -f setup_permissions.sql
```

## Verificacion

Despues de ejecutar la configuracion, verificar que los grupos fueron creados:

### En Django Admin
1. Acceder a Django Admin: `https://your-service-url/admin/`
2. Ir a "Authentication and Authorization" > "Groups"
3. Verificar que existen los 7 grupos mencionados

### Usando Django Shell
```python
from django.contrib.auth.models import Group
for group_name in ['Administradores', 'Medicos', 'Enfermeros', 'Recepcionistas',
                   'Tecnicos_Laboratorio', 'Auditores_Medicos', 'Farmaceuticos']:
    exists = Group.objects.filter(name=group_name).exists()
    print(f'{group_name}: {exists}')
```

## Asignacion de Usuarios a Grupos

### Usando Django Admin
1. Ir a "Authentication and Authorization" > "Users"
2. Seleccionar el usuario
3. En la seccion "Permissions", asignar grupos en "Groups"

### Usando Django Shell
```python
from django.contrib.auth.models import User, Group

# Obtener usuario y grupo
user = User.objects.get(username='nombre_usuario')
group = Group.objects.get(name='Medicos')

# Asignar usuario al grupo
user.groups.add(group)

# Verificar permisos
user.has_perm('can_view_patient_history')  # True si es medico
```

### Usando Codigo Python
```python
from django.contrib.auth.models import User, Group

def assign_user_to_role(username, role_name):
    """Asignar usuario a un rol especifico"""
    try:
        user = User.objects.get(username=username)
        group = Group.objects.get(name=role_name)
        user.groups.add(group)
        return True
    except (User.DoesNotExist, Group.DoesNotExist):
        return False

# Ejemplos de uso
assign_user_to_role('dr_smith', 'Medicos')
assign_user_to_role('nurse_jones', 'Enfermeros')
assign_user_to_role('admin_user', 'Administradores')
```

## Verificacion de Permisos en Views

### Usando Decoradores
```python
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test

def is_doctor(user):
    return user.groups.filter(name='Medicos').exists()

@permission_required('can_view_patient_history')
def view_patient_history(request, patient_id):
    # Solo usuarios con permiso pueden acceder
    pass

@user_passes_test(is_doctor)
def doctor_dashboard(request):
    # Solo medicos pueden acceder
    pass
```

### Usando Class-Based Views
```python
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

class PatientHistoryView(PermissionRequiredMixin, ListView):
    permission_required = 'can_view_patient_history'
    model = Patient
```

### Verificacion Manual
```python
def my_view(request):
    if request.user.has_perm('can_approve_surgeries'):
        # Usuario puede aprobar cirugias
        pass

    if request.user.groups.filter(name='Medicos').exists():
        # Usuario es medico
        pass
```

## Permisos Personalizados

Los siguientes permisos personalizados estan disponibles:

### Permisos Medicos
- `can_view_patient_history`: Ver historial medico
- `can_create_prescriptions`: Crear prescripciones
- `can_approve_surgeries`: Aprobar cirugias
- `can_view_medical_records`: Ver registros medicos
- `can_update_patient_status`: Actualizar estado de pacientes
- `can_schedule_surgeries`: Programar cirugias
- `can_access_lab_results`: Acceder a resultados de laboratorio
- `can_modify_treatments`: Modificar tratamientos

### Permisos de Enfermeria
- `can_update_patient_vitals`: Actualizar signos vitales
- `can_administer_medications`: Administrar medicamentos
- `can_view_patient_schedule`: Ver horarios de pacientes
- `can_update_patient_notes`: Actualizar notas de pacientes
- `can_assist_procedures`: Asistir en procedimientos
- `can_access_patient_records`: Acceder a registros de pacientes

### Permisos Administrativos
- `can_schedule_appointments`: Programar citas
- `can_manage_patient_info`: Gestionar informacion de pacientes
- `can_handle_billing`: Manejar facturacion
- `can_generate_reports`: Generar reportes
- `can_view_schedules`: Ver horarios
- `can_update_contact_info`: Actualizar informacion de contacto

### Permisos de Laboratorio
- `can_process_lab_samples`: Procesar muestras
- `can_update_lab_results`: Actualizar resultados
- `can_manage_equipment`: Gestionar equipos
- `can_generate_lab_reports`: Generar reportes de laboratorio
- `can_quality_control`: Control de calidad

### Permisos de Auditoria
- `can_review_medical_records`: Revisar registros para auditoria
- `can_audit_procedures`: Auditar procedimientos
- `can_generate_audit_reports`: Generar reportes de auditoria
- `can_access_compliance_data`: Acceder a datos de cumplimiento
- `can_review_billing`: Revisar facturacion

### Permisos de Farmacia
- `can_dispense_medications`: Dispensar medicamentos
- `can_manage_inventory`: Gestionar inventario
- `can_verify_prescriptions`: Verificar prescripciones
- `can_counsel_patients`: Asesorar pacientes
- `can_track_medication_usage`: Rastrear uso de medicamentos

### Permisos de Super Admin
- `can_manage_all_users`: Gestionar todos los usuarios
- `can_view_all_reports`: Ver todos los reportes
- `can_configure_system`: Configurar sistema
- `can_access_admin_panel`: Acceder al panel de admin
- `can_manage_permissions`: Gestionar permisos

## Troubleshooting

### Error: Permission DoesNotExist
Si aparece un error de que un permiso no existe:
1. Verificar que se ejecuto el setup correctamente
2. Ejecutar migraciones: `python manage.py migrate`
3. Re-ejecutar setup: `python manage.py setup_permissions --force`

### Grupos no aparecen
1. Verificar conexion a base de datos
2. Verificar que Django admin este habilitado
3. Ejecutar: `python manage.py collectstatic`

### Usuario no tiene permisos esperados
1. Verificar que el usuario este asignado al grupo correcto
2. Verificar que el grupo tenga los permisos correctos
3. Cerrar sesion y volver a iniciar sesion

## Archivos Generados

- `setup_permissions.py`: Comando de Django management
- `setup_permissions.sql`: Script SQL directo
- `setup_permissions_cloud_run.sh`: Script para Cloud Run
- `run_permissions_setup.sh`: Script local de Django
- `permissions_usage_examples.py`: Ejemplos de uso

## Contacto

Para preguntas sobre el sistema de permisos, contactar al equipo de desarrollo.
