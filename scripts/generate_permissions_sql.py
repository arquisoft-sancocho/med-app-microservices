#!/usr/bin/env python3
"""
Script para generar comandos SQL para configurar grupos y permisos del sistema medico.
Este script genera un archivo SQL que puede ejecutarse directamente en la base de datos.
"""

def generate_permissions_sql():
    """Genera comandos SQL para crear grupos y permisos"""

    # Definir grupos y sus permisos
    groups_permissions = {
        'Administradores': [
            'add_user', 'change_user', 'delete_user', 'view_user',
            'add_group', 'change_group', 'delete_group', 'view_group',
            'add_permission', 'change_permission', 'delete_permission', 'view_permission',
            'can_manage_all_users', 'can_view_all_reports', 'can_configure_system',
            'can_access_admin_panel', 'can_manage_permissions'
        ],
        'Medicos': [
            'can_view_patient_history', 'can_create_prescriptions', 'can_approve_surgeries',
            'can_view_medical_records', 'can_update_patient_status', 'can_schedule_surgeries',
            'can_access_lab_results', 'can_modify_treatments'
        ],
        'Enfermeros': [
            'can_update_patient_vitals', 'can_administer_medications', 'can_view_patient_schedule',
            'can_update_patient_notes', 'can_assist_procedures', 'can_access_patient_records'
        ],
        'Recepcionistas': [
            'can_schedule_appointments', 'can_manage_patient_info', 'can_handle_billing',
            'can_generate_reports', 'can_view_schedules', 'can_update_contact_info'
        ],
        'Tecnicos_Laboratorio': [
            'can_process_lab_samples', 'can_update_lab_results', 'can_manage_equipment',
            'can_generate_lab_reports', 'can_quality_control'
        ],
        'Auditores_Medicos': [
            'can_review_medical_records', 'can_audit_procedures', 'can_generate_audit_reports',
            'can_access_compliance_data', 'can_review_billing'
        ],
        'Farmaceuticos': [
            'can_dispense_medications', 'can_manage_inventory', 'can_verify_prescriptions',
            'can_counsel_patients', 'can_track_medication_usage'
        ]
    }

    # Permisos personalizados con descripciones
    custom_permissions = [
        ('can_view_patient_history', 'Can view patient medical history'),
        ('can_create_prescriptions', 'Can create medical prescriptions'),
        ('can_approve_surgeries', 'Can approve surgery procedures'),
        ('can_view_medical_records', 'Can view medical records'),
        ('can_update_patient_status', 'Can update patient status'),
        ('can_schedule_surgeries', 'Can schedule surgery procedures'),
        ('can_access_lab_results', 'Can access laboratory results'),
        ('can_modify_treatments', 'Can modify patient treatments'),
        ('can_update_patient_vitals', 'Can update patient vital signs'),
        ('can_administer_medications', 'Can administer medications'),
        ('can_view_patient_schedule', 'Can view patient schedules'),
        ('can_update_patient_notes', 'Can update patient notes'),
        ('can_assist_procedures', 'Can assist in medical procedures'),
        ('can_access_patient_records', 'Can access patient records'),
        ('can_schedule_appointments', 'Can schedule patient appointments'),
        ('can_manage_patient_info', 'Can manage patient information'),
        ('can_handle_billing', 'Can handle billing and payments'),
        ('can_generate_reports', 'Can generate system reports'),
        ('can_view_schedules', 'Can view appointment schedules'),
        ('can_update_contact_info', 'Can update contact information'),
        ('can_process_lab_samples', 'Can process laboratory samples'),
        ('can_update_lab_results', 'Can update laboratory results'),
        ('can_manage_equipment', 'Can manage medical equipment'),
        ('can_generate_lab_reports', 'Can generate laboratory reports'),
        ('can_quality_control', 'Can perform quality control'),
        ('can_review_medical_records', 'Can review medical records for audit'),
        ('can_audit_procedures', 'Can audit medical procedures'),
        ('can_generate_audit_reports', 'Can generate audit reports'),
        ('can_access_compliance_data', 'Can access compliance data'),
        ('can_review_billing', 'Can review billing information'),
        ('can_dispense_medications', 'Can dispense medications'),
        ('can_manage_inventory', 'Can manage pharmacy inventory'),
        ('can_verify_prescriptions', 'Can verify medical prescriptions'),
        ('can_counsel_patients', 'Can provide patient counseling'),
        ('can_track_medication_usage', 'Can track medication usage'),
        ('can_manage_all_users', 'Can manage all system users'),
        ('can_view_all_reports', 'Can view all system reports'),
        ('can_configure_system', 'Can configure system settings'),
        ('can_access_admin_panel', 'Can access administration panel'),
        ('can_manage_permissions', 'Can manage user permissions')
    ]

    sql_commands = []

    # Encabezado
    sql_commands.append("-- Medical System Permissions Setup Script")
    sql_commands.append("-- Generated automatically - Run in Django database")
    sql_commands.append("-- Date: $(date)")
    sql_commands.append("")

    # Obtener content_type_id para auth.user
    sql_commands.append("-- Get content type ID for auth.user model")
    sql_commands.append("DO $$")
    sql_commands.append("DECLARE")
    sql_commands.append("    user_content_type_id INTEGER;")
    sql_commands.append("    group_id INTEGER;")
    sql_commands.append("    permission_id INTEGER;")
    sql_commands.append("BEGIN")
    sql_commands.append("")

    # Obtener content_type_id
    sql_commands.append("    -- Get user content type ID")
    sql_commands.append("    SELECT id INTO user_content_type_id")
    sql_commands.append("    FROM django_content_type")
    sql_commands.append("    WHERE app_label = 'auth' AND model = 'user';")
    sql_commands.append("")

    # Crear permisos personalizados
    sql_commands.append("    -- Create custom permissions")
    for codename, name in custom_permissions:
        sql_commands.append(f"    -- Permission: {codename}")
        sql_commands.append("    INSERT INTO auth_permission (name, content_type_id, codename)")
        sql_commands.append(f"    VALUES ('{name}', user_content_type_id, '{codename}')")
        sql_commands.append("    ON CONFLICT (content_type_id, codename) DO NOTHING;")
        sql_commands.append("")

    # Crear grupos y asignar permisos
    for group_name, permission_codenames in groups_permissions.items():
        sql_commands.append(f"    -- Create group: {group_name}")
        sql_commands.append("    INSERT INTO auth_group (name)")
        sql_commands.append(f"    VALUES ('{group_name}')")
        sql_commands.append("    ON CONFLICT (name) DO NOTHING;")
        sql_commands.append("")

        sql_commands.append(f"    -- Get group ID for {group_name}")
        sql_commands.append("    SELECT id INTO group_id")
        sql_commands.append("    FROM auth_group")
        sql_commands.append(f"    WHERE name = '{group_name}';")
        sql_commands.append("")

        # Asignar permisos al grupo
        sql_commands.append(f"    -- Assign permissions to {group_name}")
        for permission_codename in permission_codenames:
            sql_commands.append(f"    -- Add permission: {permission_codename}")
            sql_commands.append("    SELECT id INTO permission_id")
            sql_commands.append("    FROM auth_permission")
            sql_commands.append(f"    WHERE codename = '{permission_codename}';")
            sql_commands.append("")
            sql_commands.append("    IF permission_id IS NOT NULL THEN")
            sql_commands.append("        INSERT INTO auth_group_permissions (group_id, permission_id)")
            sql_commands.append("        VALUES (group_id, permission_id)")
            sql_commands.append("        ON CONFLICT (group_id, permission_id) DO NOTHING;")
            sql_commands.append("    END IF;")
            sql_commands.append("")

    sql_commands.append("END $$;")
    sql_commands.append("")

    # Agregar consultas de verificacion
    sql_commands.append("-- Verification queries")
    sql_commands.append("SELECT 'Groups created:' as info, count(*) as count FROM auth_group;")
    sql_commands.append("SELECT 'Custom permissions created:' as info, count(*) as count FROM auth_permission WHERE codename LIKE 'can_%';")
    sql_commands.append("")
    sql_commands.append("-- Group summary")
    sql_commands.append("SELECT")
    sql_commands.append("    g.name as group_name,")
    sql_commands.append("    count(gp.permission_id) as permission_count")
    sql_commands.append("FROM auth_group g")
    sql_commands.append("LEFT JOIN auth_group_permissions gp ON g.id = gp.group_id")
    sql_commands.append("GROUP BY g.name")
    sql_commands.append("ORDER BY g.name;")

    return '\n'.join(sql_commands)

def generate_django_commands():
    """Genera comandos de Django para usar con manage.py"""

    groups_permissions = {
        'Administradores': [
            'add_user', 'change_user', 'delete_user', 'view_user',
            'add_group', 'change_group', 'delete_group', 'view_group',
            'add_permission', 'change_permission', 'delete_permission', 'view_permission',
            'can_manage_all_users', 'can_view_all_reports', 'can_configure_system',
            'can_access_admin_panel', 'can_manage_permissions'
        ],
        'Medicos': [
            'can_view_patient_history', 'can_create_prescriptions', 'can_approve_surgeries',
            'can_view_medical_records', 'can_update_patient_status', 'can_schedule_surgeries',
            'can_access_lab_results', 'can_modify_treatments'
        ],
        'Enfermeros': [
            'can_update_patient_vitals', 'can_administer_medications', 'can_view_patient_schedule',
            'can_update_patient_notes', 'can_assist_procedures', 'can_access_patient_records'
        ],
        'Recepcionistas': [
            'can_schedule_appointments', 'can_manage_patient_info', 'can_handle_billing',
            'can_generate_reports', 'can_view_schedules', 'can_update_contact_info'
        ],
        'Tecnicos_Laboratorio': [
            'can_process_lab_samples', 'can_update_lab_results', 'can_manage_equipment',
            'can_generate_lab_reports', 'can_quality_control'
        ],
        'Auditores_Medicos': [
            'can_review_medical_records', 'can_audit_procedures', 'can_generate_audit_reports',
            'can_access_compliance_data', 'can_review_billing'
        ],
        'Farmaceuticos': [
            'can_dispense_medications', 'can_manage_inventory', 'can_verify_prescriptions',
            'can_counsel_patients', 'can_track_medication_usage'
        ]
    }

    commands = []
    commands.append("#!/bin/bash")
    commands.append("# Django commands to setup permissions")
    commands.append("# Run this from the Django project directory")
    commands.append("")
    commands.append("echo 'Setting up medical system permissions...'")
    commands.append("")
    commands.append("# Run the custom management command")
    commands.append("python manage.py setup_permissions")
    commands.append("")
    commands.append("echo 'Permissions setup completed!'")
    commands.append("")
    commands.append("# Verify groups were created")
    commands.append("echo 'Created groups:'")
    for group_name in groups_permissions.keys():
        commands.append(f"python manage.py shell -c \"from django.contrib.auth.models import Group; print(f'{group_name}: {{Group.objects.filter(name='{group_name}').exists()}}')\"")

    return '\n'.join(commands)

if __name__ == "__main__":
    import os
    import datetime

    # Crear directorio de salida si no existe
    output_dir = "/home/db/University/arquisoft/med-app-microservices/scripts"
    os.makedirs(output_dir, exist_ok=True)

    # Generar archivo SQL
    sql_content = generate_permissions_sql()
    sql_file = os.path.join(output_dir, "setup_permissions.sql")

    with open(sql_file, 'w', encoding='utf-8') as f:
        f.write(sql_content.replace("$(date)", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    print(f"SQL script generated: {sql_file}")

    # Generar archivo de comandos Django
    django_content = generate_django_commands()
    django_file = os.path.join(output_dir, "run_permissions_setup.sh")

    with open(django_file, 'w', encoding='utf-8') as f:
        f.write(django_content)

    # Hacer ejecutable el script
    os.chmod(django_file, 0o755)

    print(f"Django commands script generated: {django_file}")
    print("\nTo execute:")
    print(f"1. For SQL: psql -d your_database -f {sql_file}")
    print(f"2. For Django: {django_file}")
    print("\nBoth scripts create the same permissions structure.")
