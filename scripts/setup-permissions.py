#!/usr/bin/env python
"""
Setup script for Django permissions and groups in Medical System
Creates user groups and assigns appropriate permissions for medical staff roles.
"""
import os
import sys
import django

# Add the project root to Python path
sys.path.append('/home/db/University/arquisoft/med-app-microservices')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_system.settings')

# Setup Django
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.apps import apps

def create_permissions_and_groups():
    """Create all necessary groups and permissions for the medical system"""
    
    print("🏥 Setting up Medical System Permissions and Groups...")
    print("=" * 60)
    
    # Define groups and their permissions
    groups_permissions = {
        'Administradores': {
            'description': 'Administradores del sistema con acceso completo',
            'permissions': [
                # User management
                'auth.add_user', 'auth.change_user', 'auth.delete_user', 'auth.view_user',
                'auth.add_group', 'auth.change_group', 'auth.delete_group', 'auth.view_group',
                'auth.add_permission', 'auth.change_permission', 'auth.delete_permission', 'auth.view_permission',
                
                # Patient management - full access
                'pacientes2.add_paciente2', 'pacientes2.change_paciente2', 
                'pacientes2.delete_paciente2', 'pacientes2.view_paciente2',
                
                # Exams - full access
                'examenes2.add_examen2', 'examenes2.change_examen2', 
                'examenes2.delete_examen2', 'examenes2.view_examen2',
                
                # Diagnosis - full access
                'diagnosticos2.add_diagnostico2', 'diagnosticos2.change_diagnostico2', 
                'diagnosticos2.delete_diagnostico2', 'diagnosticos2.view_diagnostico2',
                
                # Surgery - full access
                'cirugias.add_cirugia', 'cirugias.change_cirugia', 
                'cirugias.delete_cirugia', 'cirugias.view_cirugia',
                
                # Consultations - full access
                'consultas.add_consulta', 'consultas.change_consulta', 
                'consultas.delete_consulta', 'consultas.view_consulta',
            ]
        },
        
        'Médicos': {
            'description': 'Médicos con acceso completo a pacientes y procedimientos',
            'permissions': [
                # Patient management - full access
                'pacientes2.add_paciente2', 'pacientes2.change_paciente2', 'pacientes2.view_paciente2',
                
                # Exams - full access
                'examenes2.add_examen2', 'examenes2.change_examen2', 'examenes2.view_examen2',
                
                # Diagnosis - full access
                'diagnosticos2.add_diagnostico2', 'diagnosticos2.change_diagnostico2', 'diagnosticos2.view_diagnostico2',
                
                # Surgery - full access
                'cirugias.add_cirugia', 'cirugias.change_cirugia', 'cirugias.view_cirugia',
                
                # Consultations - full access
                'consultas.add_consulta', 'consultas.change_consulta', 'consultas.view_consulta',
            ]
        },
        
        'Enfermeros': {
            'description': 'Enfermeros con acceso limitado a pacientes y procedimientos',
            'permissions': [
                # Patient management - view and limited edit
                'pacientes2.view_paciente2', 'pacientes2.change_paciente2',
                
                # Exams - view and add
                'examenes2.add_examen2', 'examenes2.view_examen2',
                
                # Diagnosis - view only
                'diagnosticos2.view_diagnostico2',
                
                # Surgery - view only
                'cirugias.view_cirugia',
                
                # Consultations - view and add
                'consultas.add_consulta', 'consultas.view_consulta',
            ]
        },
        
        'Recepcionistas': {
            'description': 'Personal de recepción con acceso básico',
            'permissions': [
                # Patient management - add and view
                'pacientes2.add_paciente2', 'pacientes2.view_paciente2', 'pacientes2.change_paciente2',
                
                # Consultations - schedule and view
                'consultas.add_consulta', 'consultas.view_consulta', 'consultas.change_consulta',
                
                # Exams - view only
                'examenes2.view_examen2',
                
                # Basic view access to other modules
                'diagnosticos2.view_diagnostico2',
                'cirugias.view_cirugia',
            ]
        },
        
        'Técnicos_Laboratorio': {
            'description': 'Técnicos de laboratorio con acceso a exámenes',
            'permissions': [
                # Patient information - view only
                'pacientes2.view_paciente2',
                
                # Exams - full access
                'examenes2.add_examen2', 'examenes2.change_examen2', 'examenes2.view_examen2',
                
                # Limited view access
                'diagnosticos2.view_diagnostico2',
            ]
        },
        
        'Auditores_Médicos': {
            'description': 'Personal de auditoría con acceso de solo lectura',
            'permissions': [
                # Read-only access to all medical data
                'pacientes2.view_paciente2',
                'examenes2.view_examen2',
                'diagnosticos2.view_diagnostico2',
                'cirugias.view_cirugia',
                'consultas.view_consulta',
            ]
        },
        
        'Farmacéuticos': {
            'description': 'Farmacéuticos con acceso a diagnósticos y tratamientos',
            'permissions': [
                # Patient information - view only
                'pacientes2.view_paciente2',
                
                # Diagnosis and treatments - view and modify treatments
                'diagnosticos2.view_diagnostico2', 'diagnosticos2.change_diagnostico2',
                
                # Limited access to other modules
                'consultas.view_consulta',
                'examenes2.view_examen2',
            ]
        }
    }
    
    # Custom permissions to create
    custom_permissions = [
        {
            'codename': 'can_view_patient_history',
            'name': 'Can view complete patient medical history',
            'content_type': 'pacientes2.paciente2'
        },
        {
            'codename': 'can_access_emergency_data',
            'name': 'Can access emergency patient data',
            'content_type': 'pacientes2.paciente2'
        },
        {
            'codename': 'can_approve_surgeries',
            'name': 'Can approve surgery procedures',
            'content_type': 'cirugias.cirugia'
        },
        {
            'codename': 'can_manage_lab_results',
            'name': 'Can manage laboratory results',
            'content_type': 'examenes2.examen2'
        },
        {
            'codename': 'can_prescribe_treatments',
            'name': 'Can prescribe medical treatments',
            'content_type': 'diagnosticos2.diagnostico2'
        },
        {
            'codename': 'can_schedule_appointments',
            'name': 'Can schedule patient appointments',
            'content_type': 'consultas.consulta'
        },
        {
            'codename': 'can_access_billing',
            'name': 'Can access billing information',
            'content_type': 'consultas.consulta'
        }
    ]
    
    print("📋 Creating custom permissions...")
    created_custom_permissions = []
    
    for perm_data in custom_permissions:
        try:
            # Get the content type
            app_label, model_name = perm_data['content_type'].split('.')
            content_type = ContentType.objects.get(app_label=app_label, model=model_name)
            
            # Create or get the permission
            permission, created = Permission.objects.get_or_create(
                codename=perm_data['codename'],
                content_type=content_type,
                defaults={'name': perm_data['name']}
            )
            
            if created:
                print(f"  ✅ Created: {permission.name}")
                created_custom_permissions.append(permission)
            else:
                print(f"  ⚠️  Already exists: {permission.name}")
                
        except ContentType.DoesNotExist:
            print(f"  ❌ Content type not found: {perm_data['content_type']}")
        except Exception as e:
            print(f"  ❌ Error creating permission {perm_data['codename']}: {str(e)}")
    
    print(f"\n👥 Creating groups and assigning permissions...")
    
    for group_name, group_data in groups_permissions.items():
        # Create or get the group
        group, created = Group.objects.get_or_create(name=group_name)
        
        if created:
            print(f"\n✅ Created group: {group_name}")
        else:
            print(f"\n⚠️  Group already exists: {group_name}")
            # Clear existing permissions to reassign
            group.permissions.clear()
        
        print(f"   📝 {group_data['description']}")
        
        # Assign permissions to the group
        assigned_count = 0
        for perm_codename in group_data['permissions']:
            try:
                # Handle both app.perm and just perm formats
                if '.' in perm_codename:
                    app_label, codename = perm_codename.split('.', 1)
                    permission = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename
                    )
                else:
                    permission = Permission.objects.get(codename=perm_codename)
                
                group.permissions.add(permission)
                assigned_count += 1
                
            except Permission.DoesNotExist:
                print(f"      ❌ Permission not found: {perm_codename}")
            except Exception as e:
                print(f"      ❌ Error assigning permission {perm_codename}: {str(e)}")
        
        print(f"   📊 Assigned {assigned_count} permissions")
        
        # Add custom permissions for specific groups
        if group_name == 'Médicos':
            for perm in ['can_view_patient_history', 'can_approve_surgeries', 'can_prescribe_treatments']:
                try:
                    permission = Permission.objects.get(codename=perm)
                    group.permissions.add(permission)
                    print(f"      ➕ Added custom permission: {perm}")
                except Permission.DoesNotExist:
                    pass
                    
        elif group_name == 'Administradores':
            # Add all custom permissions to administrators
            for permission in created_custom_permissions:
                group.permissions.add(permission)
            print(f"      ➕ Added all custom permissions")
            
        elif group_name == 'Enfermeros':
            for perm in ['can_access_emergency_data', 'can_schedule_appointments']:
                try:
                    permission = Permission.objects.get(codename=perm)
                    group.permissions.add(permission)
                    print(f"      ➕ Added custom permission: {perm}")
                except Permission.DoesNotExist:
                    pass
                    
        elif group_name == 'Técnicos_Laboratorio':
            try:
                permission = Permission.objects.get(codename='can_manage_lab_results')
                group.permissions.add(permission)
                print(f"      ➕ Added custom permission: can_manage_lab_results")
            except Permission.DoesNotExist:
                pass
                
        elif group_name == 'Recepcionistas':
            for perm in ['can_schedule_appointments', 'can_access_billing']:
                try:
                    permission = Permission.objects.get(codename=perm)
                    group.permissions.add(permission)
                    print(f"      ➕ Added custom permission: {perm}")
                except Permission.DoesNotExist:
                    pass
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY:")
    print(f"✅ Groups created/updated: {len(groups_permissions)}")
    print(f"✅ Custom permissions created: {len(created_custom_permissions)}")
    
    print("\n🔒 Security Guidelines:")
    print("• Assign users to appropriate groups based on their role")
    print("• Regularly review and audit user permissions")
    print("• Use the principle of least privilege")
    print("• Consider creating additional custom permissions as needed")
    
    print("\n👥 Available Groups:")
    for group_name, group_data in groups_permissions.items():
        group = Group.objects.get(name=group_name)
        perm_count = group.permissions.count()
        print(f"• {group_name}: {perm_count} permissions - {group_data['description']}")
    
    print("\n🏥 Medical System permissions setup completed successfully! 🎉")

if __name__ == "__main__":
    try:
        create_permissions_and_groups()
    except Exception as e:
        print(f"❌ Error setting up permissions: {str(e)}")
        sys.exit(1)
