from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Setup medical system groups and permissions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of groups and permissions',
        )

    def handle(self, *args, **options):
        force = options['force']

        self.stdout.write('Starting permissions setup...')

        # Define groups and their permissions
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

        # Create custom permissions
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

        try:
            # Get User content type for custom permissions
            user_content_type = ContentType.objects.get_for_model(
                apps.get_model('auth', 'User')
            )

            # Create custom permissions
            created_permissions = 0
            for codename, name in custom_permissions:
                permission, created = Permission.objects.get_or_create(
                    codename=codename,
                    content_type=user_content_type,
                    defaults={'name': name}
                )
                if created:
                    created_permissions += 1
                    self.stdout.write(f'Created permission: {codename}')
                elif force:
                    permission.name = name
                    permission.save()
                    self.stdout.write(f'Updated permission: {codename}')

            self.stdout.write(f'Custom permissions processed: {created_permissions} created')

            # Create groups and assign permissions
            created_groups = 0
            for group_name, permission_codenames in groups_permissions.items():
                group, created = Group.objects.get_or_create(name=group_name)

                if created:
                    created_groups += 1
                    self.stdout.write(f'Created group: {group_name}')
                elif force:
                    group.permissions.clear()
                    self.stdout.write(f'Cleared permissions for group: {group_name}')

                # Assign permissions to group
                permissions_added = 0
                for permission_codename in permission_codenames:
                    try:
                        permission = Permission.objects.get(codename=permission_codename)
                        if permission not in group.permissions.all() or force:
                            group.permissions.add(permission)
                            permissions_added += 1
                    except Permission.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Permission "{permission_codename}" not found for group "{group_name}"'
                            )
                        )

                self.stdout.write(f'Added {permissions_added} permissions to {group_name}')

            self.stdout.write(
                self.style.SUCCESS(
                    f'Permission setup completed successfully!\n'
                    f'Groups processed: {len(groups_permissions)}\n'
                    f'New groups created: {created_groups}\n'
                    f'Custom permissions created: {created_permissions}'
                )
            )

            # Display group summary
            self.stdout.write('\n=== GROUP SUMMARY ===')
            for group_name in groups_permissions.keys():
                try:
                    group = Group.objects.get(name=group_name)
                    permission_count = group.permissions.count()
                    self.stdout.write(f'{group_name}: {permission_count} permissions')
                except Group.DoesNotExist:
                    self.stdout.write(f'{group_name}: NOT FOUND')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during permission setup: {str(e)}')
            )
            logger.error(f'Permission setup failed: {str(e)}')
            raise
