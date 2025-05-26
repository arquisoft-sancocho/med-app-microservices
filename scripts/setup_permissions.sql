-- Medical System Permissions Setup Script
-- Generated automatically - Run in Django database
-- Date: 2025-05-26 00:31:05

-- Get content type ID for auth.user model
DO $$
DECLARE
    user_content_type_id INTEGER;
    group_id INTEGER;
    permission_id INTEGER;
BEGIN

    -- Get user content type ID
    SELECT id INTO user_content_type_id
    FROM django_content_type
    WHERE app_label = 'auth' AND model = 'user';

    -- Create custom permissions
    -- Permission: can_view_patient_history
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can view patient medical history', user_content_type_id, 'can_view_patient_history')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_create_prescriptions
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can create medical prescriptions', user_content_type_id, 'can_create_prescriptions')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_approve_surgeries
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can approve surgery procedures', user_content_type_id, 'can_approve_surgeries')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_view_medical_records
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can view medical records', user_content_type_id, 'can_view_medical_records')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_update_patient_status
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can update patient status', user_content_type_id, 'can_update_patient_status')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_schedule_surgeries
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can schedule surgery procedures', user_content_type_id, 'can_schedule_surgeries')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_access_lab_results
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can access laboratory results', user_content_type_id, 'can_access_lab_results')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_modify_treatments
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can modify patient treatments', user_content_type_id, 'can_modify_treatments')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_update_patient_vitals
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can update patient vital signs', user_content_type_id, 'can_update_patient_vitals')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_administer_medications
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can administer medications', user_content_type_id, 'can_administer_medications')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_view_patient_schedule
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can view patient schedules', user_content_type_id, 'can_view_patient_schedule')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_update_patient_notes
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can update patient notes', user_content_type_id, 'can_update_patient_notes')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_assist_procedures
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can assist in medical procedures', user_content_type_id, 'can_assist_procedures')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_access_patient_records
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can access patient records', user_content_type_id, 'can_access_patient_records')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_schedule_appointments
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can schedule patient appointments', user_content_type_id, 'can_schedule_appointments')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_manage_patient_info
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can manage patient information', user_content_type_id, 'can_manage_patient_info')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_handle_billing
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can handle billing and payments', user_content_type_id, 'can_handle_billing')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_generate_reports
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can generate system reports', user_content_type_id, 'can_generate_reports')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_view_schedules
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can view appointment schedules', user_content_type_id, 'can_view_schedules')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_update_contact_info
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can update contact information', user_content_type_id, 'can_update_contact_info')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_process_lab_samples
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can process laboratory samples', user_content_type_id, 'can_process_lab_samples')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_update_lab_results
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can update laboratory results', user_content_type_id, 'can_update_lab_results')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_manage_equipment
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can manage medical equipment', user_content_type_id, 'can_manage_equipment')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_generate_lab_reports
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can generate laboratory reports', user_content_type_id, 'can_generate_lab_reports')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_quality_control
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can perform quality control', user_content_type_id, 'can_quality_control')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_review_medical_records
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can review medical records for audit', user_content_type_id, 'can_review_medical_records')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_audit_procedures
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can audit medical procedures', user_content_type_id, 'can_audit_procedures')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_generate_audit_reports
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can generate audit reports', user_content_type_id, 'can_generate_audit_reports')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_access_compliance_data
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can access compliance data', user_content_type_id, 'can_access_compliance_data')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_review_billing
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can review billing information', user_content_type_id, 'can_review_billing')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_dispense_medications
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can dispense medications', user_content_type_id, 'can_dispense_medications')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_manage_inventory
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can manage pharmacy inventory', user_content_type_id, 'can_manage_inventory')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_verify_prescriptions
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can verify medical prescriptions', user_content_type_id, 'can_verify_prescriptions')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_counsel_patients
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can provide patient counseling', user_content_type_id, 'can_counsel_patients')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_track_medication_usage
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can track medication usage', user_content_type_id, 'can_track_medication_usage')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_manage_all_users
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can manage all system users', user_content_type_id, 'can_manage_all_users')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_view_all_reports
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can view all system reports', user_content_type_id, 'can_view_all_reports')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_configure_system
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can configure system settings', user_content_type_id, 'can_configure_system')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_access_admin_panel
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can access administration panel', user_content_type_id, 'can_access_admin_panel')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Permission: can_manage_permissions
    INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can manage user permissions', user_content_type_id, 'can_manage_permissions')
    ON CONFLICT (content_type_id, codename) DO NOTHING;

    -- Create group: Administradores
    INSERT INTO auth_group (name)
    VALUES ('Administradores')
    ON CONFLICT (name) DO NOTHING;

    -- Get group ID for Administradores
    SELECT id INTO group_id
    FROM auth_group
    WHERE name = 'Administradores';

    -- Assign permissions to Administradores
    -- Add permission: add_user
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'add_user';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: change_user
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'change_user';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: delete_user
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'delete_user';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: view_user
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'view_user';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: add_group
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'add_group';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: change_group
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'change_group';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: delete_group
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'delete_group';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: view_group
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'view_group';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: add_permission
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'add_permission';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: change_permission
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'change_permission';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: delete_permission
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'delete_permission';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: view_permission
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'view_permission';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_manage_all_users
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_manage_all_users';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_view_all_reports
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_view_all_reports';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_configure_system
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_configure_system';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_access_admin_panel
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_access_admin_panel';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_manage_permissions
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_manage_permissions';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Create group: Medicos
    INSERT INTO auth_group (name)
    VALUES ('Medicos')
    ON CONFLICT (name) DO NOTHING;

    -- Get group ID for Medicos
    SELECT id INTO group_id
    FROM auth_group
    WHERE name = 'Medicos';

    -- Assign permissions to Medicos
    -- Add permission: can_view_patient_history
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_view_patient_history';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_create_prescriptions
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_create_prescriptions';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_approve_surgeries
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_approve_surgeries';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_view_medical_records
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_view_medical_records';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_update_patient_status
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_update_patient_status';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_schedule_surgeries
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_schedule_surgeries';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_access_lab_results
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_access_lab_results';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_modify_treatments
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_modify_treatments';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Create group: Enfermeros
    INSERT INTO auth_group (name)
    VALUES ('Enfermeros')
    ON CONFLICT (name) DO NOTHING;

    -- Get group ID for Enfermeros
    SELECT id INTO group_id
    FROM auth_group
    WHERE name = 'Enfermeros';

    -- Assign permissions to Enfermeros
    -- Add permission: can_update_patient_vitals
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_update_patient_vitals';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_administer_medications
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_administer_medications';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_view_patient_schedule
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_view_patient_schedule';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_update_patient_notes
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_update_patient_notes';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_assist_procedures
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_assist_procedures';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_access_patient_records
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_access_patient_records';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Create group: Recepcionistas
    INSERT INTO auth_group (name)
    VALUES ('Recepcionistas')
    ON CONFLICT (name) DO NOTHING;

    -- Get group ID for Recepcionistas
    SELECT id INTO group_id
    FROM auth_group
    WHERE name = 'Recepcionistas';

    -- Assign permissions to Recepcionistas
    -- Add permission: can_schedule_appointments
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_schedule_appointments';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_manage_patient_info
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_manage_patient_info';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_handle_billing
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_handle_billing';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_generate_reports
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_generate_reports';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_view_schedules
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_view_schedules';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_update_contact_info
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_update_contact_info';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Create group: Tecnicos_Laboratorio
    INSERT INTO auth_group (name)
    VALUES ('Tecnicos_Laboratorio')
    ON CONFLICT (name) DO NOTHING;

    -- Get group ID for Tecnicos_Laboratorio
    SELECT id INTO group_id
    FROM auth_group
    WHERE name = 'Tecnicos_Laboratorio';

    -- Assign permissions to Tecnicos_Laboratorio
    -- Add permission: can_process_lab_samples
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_process_lab_samples';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_update_lab_results
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_update_lab_results';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_manage_equipment
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_manage_equipment';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_generate_lab_reports
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_generate_lab_reports';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_quality_control
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_quality_control';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Create group: Auditores_Medicos
    INSERT INTO auth_group (name)
    VALUES ('Auditores_Medicos')
    ON CONFLICT (name) DO NOTHING;

    -- Get group ID for Auditores_Medicos
    SELECT id INTO group_id
    FROM auth_group
    WHERE name = 'Auditores_Medicos';

    -- Assign permissions to Auditores_Medicos
    -- Add permission: can_review_medical_records
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_review_medical_records';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_audit_procedures
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_audit_procedures';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_generate_audit_reports
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_generate_audit_reports';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_access_compliance_data
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_access_compliance_data';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_review_billing
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_review_billing';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Create group: Farmaceuticos
    INSERT INTO auth_group (name)
    VALUES ('Farmaceuticos')
    ON CONFLICT (name) DO NOTHING;

    -- Get group ID for Farmaceuticos
    SELECT id INTO group_id
    FROM auth_group
    WHERE name = 'Farmaceuticos';

    -- Assign permissions to Farmaceuticos
    -- Add permission: can_dispense_medications
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_dispense_medications';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_manage_inventory
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_manage_inventory';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_verify_prescriptions
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_verify_prescriptions';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_counsel_patients
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_counsel_patients';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

    -- Add permission: can_track_medication_usage
    SELECT id INTO permission_id
    FROM auth_permission
    WHERE codename = 'can_track_medication_usage';

    IF permission_id IS NOT NULL THEN
        INSERT INTO auth_group_permissions (group_id, permission_id)
        VALUES (group_id, permission_id)
        ON CONFLICT (group_id, permission_id) DO NOTHING;
    END IF;

END $$;

-- Verification queries
SELECT 'Groups created:' as info, count(*) as count FROM auth_group;
SELECT 'Custom permissions created:' as info, count(*) as count FROM auth_permission WHERE codename LIKE 'can_%';

-- Group summary
SELECT
    g.name as group_name,
    count(gp.permission_id) as permission_count
FROM auth_group g
LEFT JOIN auth_group_permissions gp ON g.id = gp.group_id
GROUP BY g.name
ORDER BY g.name;