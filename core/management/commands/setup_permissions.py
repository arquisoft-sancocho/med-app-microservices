"""
Django Management Command to setup permissions and groups
Usage: python manage.py setup_permissions
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

class Command(BaseCommand):
    help = 'Setup permissions and groups for the medical system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset all groups and permissions before creating new ones',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without making changes',
        )

    def handle(self, *args, **options):
        self.dry_run = options['dry_run']

        if self.dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )

        self.stdout.write('Setting up Medical System permissions and groups...')

        if options['reset']:
            self.reset_groups()

        with transaction.atomic():
            self.create_custom_permissions()
            self.create_groups_and_assign_permissions()

        self.stdout.write(
            self.style.SUCCESS('✅ Successfully setup permissions and groups!')
        )

    def reset_groups(self):
        """Reset all groups"""
        if self.dry_run:
            self.stdout.write('Would delete all groups')
            return

        Group.objects.all().delete()
        self.stdout.write('🗑️  Deleted all existing groups')

    def create_custom_permissions(self):
        """Create custom permissions"""
        self.stdout.write('📋 Creating custom permissions...')

        custom_permissions = [
            ('pacientes2', 'paciente2', 'can_view_patient_history', 'Can view complete patient medical history'),
            ('pacientes2', 'paciente2', 'can_access_emergency_data', 'Can access emergency patient data'),
            ('cirugias', 'cirugia', 'can_approve_surgeries', 'Can approve surgery procedures'),
            ('examenes2', 'examen2', 'can_manage_lab_results', 'Can manage laboratory results'),
            ('diagnosticos2', 'diagnostico2', 'can_prescribe_treatments', 'Can prescribe medical treatments'),
            ('consultas', 'consultamedica', 'can_schedule_appointments', 'Can schedule patient appointments'),
            ('consultas', 'consultamedica', 'can_access_billing', 'Can access billing information'),
        ]

        for app_label, model_name, codename, name in custom_permissions:
            try:
                if self.dry_run:
                    self.stdout.write(f'  Would create: {name}')
                    continue

                content_type = ContentType.objects.get(app_label=app_label, model=model_name)
                permission, created = Permission.objects.get_or_create(
                    codename=codename,
                    content_type=content_type,
                    defaults={'name': name}
                )

                if created:
                    self.stdout.write(f'  ✅ Created: {name}')
                else:
                    self.stdout.write(f'  ⚠️  Already exists: {name}')

            except ContentType.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Content type not found: {app_label}.{model_name}')
                )

    def create_groups_and_assign_permissions(self):
        """Create groups and assign permissions"""
        self.stdout.write('👥 Creating groups and assigning permissions...')

        groups_config = {
            'Administradores': {
                'permissions': [
                    # User management
                    'auth.add_user', 'auth.change_user', 'auth.delete_user', 'auth.view_user',
                    'auth.add_group', 'auth.change_group', 'auth.delete_group', 'auth.view_group',

                    # All model permissions
                    'pacientes2.add_paciente2', 'pacientes2.change_paciente2',
                    'pacientes2.delete_paciente2', 'pacientes2.view_paciente2',
                    'examenes2.add_examen2', 'examenes2.change_examen2',
                    'examenes2.delete_examen2', 'examenes2.view_examen2',
                    'diagnosticos2.add_diagnostico2', 'diagnosticos2.change_diagnostico2',
                    'diagnosticos2.delete_diagnostico2', 'diagnosticos2.view_diagnostico2',
                    'cirugias.add_cirugia', 'cirugias.change_cirugia',
                    'cirugias.delete_cirugia', 'cirugias.view_cirugia',
                    'consultas.add_consulta', 'consultas.change_consulta',
                    'consultas.delete_consulta', 'consultas.view_consulta',
                ],
                'custom_permissions': [
                    'can_view_patient_history', 'can_access_emergency_data',
                    'can_approve_surgeries', 'can_manage_lab_results',
                    'can_prescribe_treatments', 'can_schedule_appointments',
                    'can_access_billing'
                ]
            },

            'Médicos': {
                'permissions': [
                    'pacientes2.add_paciente2', 'pacientes2.change_paciente2', 'pacientes2.view_paciente2',
                    'examenes2.add_examen2', 'examenes2.change_examen2', 'examenes2.view_examen2',
                    'diagnosticos2.add_diagnostico2', 'diagnosticos2.change_diagnostico2', 'diagnosticos2.view_diagnostico2',
                    'cirugias.add_cirugia', 'cirugias.change_cirugia', 'cirugias.view_cirugia',
                    'consultas.add_consulta', 'consultas.change_consulta', 'consultas.view_consulta',
                ],
                'custom_permissions': [
                    'can_view_patient_history', 'can_approve_surgeries', 'can_prescribe_treatments'
                ]
            },

            'Enfermeros': {
                'permissions': [
                    'pacientes2.view_paciente2', 'pacientes2.change_paciente2',
                    'examenes2.add_examen2', 'examenes2.view_examen2',
                    'diagnosticos2.view_diagnostico2',
                    'cirugias.view_cirugia',
                    'consultas.add_consulta', 'consultas.view_consulta',
                ],
                'custom_permissions': [
                    'can_access_emergency_data', 'can_schedule_appointments'
                ]
            },

            'Recepcionistas': {
                'permissions': [
                    'pacientes2.add_paciente2', 'pacientes2.view_paciente2', 'pacientes2.change_paciente2',
                    'consultas.add_consulta', 'consultas.view_consulta', 'consultas.change_consulta',
                    'examenes2.view_examen2',
                    'diagnosticos2.view_diagnostico2',
                    'cirugias.view_cirugia',
                ],
                'custom_permissions': [
                    'can_schedule_appointments', 'can_access_billing'
                ]
            },

            'Técnicos_Laboratorio': {
                'permissions': [
                    'pacientes2.view_paciente2',
                    'examenes2.add_examen2', 'examenes2.change_examen2', 'examenes2.view_examen2',
                    'diagnosticos2.view_diagnostico2',
                ],
                'custom_permissions': [
                    'can_manage_lab_results'
                ]
            },

            'Auditores_Médicos': {
                'permissions': [
                    'pacientes2.view_paciente2',
                    'examenes2.view_examen2',
                    'diagnosticos2.view_diagnostico2',
                    'cirugias.view_cirugia',
                    'consultas.view_consulta',
                ],
                'custom_permissions': []
            },

            'Farmacéuticos': {
                'permissions': [
                    'pacientes2.view_paciente2',
                    'diagnosticos2.view_diagnostico2', 'diagnosticos2.change_diagnostico2',
                    'consultas.view_consulta',
                    'examenes2.view_examen2',
                ],
                'custom_permissions': [
                    'can_prescribe_treatments'
                ]
            }
        }

        for group_name, config in groups_config.items():
            if self.dry_run:
                self.stdout.write(f'\nWould create group: {group_name}')
                self.stdout.write(f'  Permissions: {len(config["permissions"])}')
                self.stdout.write(f'  Custom permissions: {len(config["custom_permissions"])}')
                continue

            # Create or get group
            group, created = Group.objects.get_or_create(name=group_name)

            if created:
                self.stdout.write(f'\n✅ Created group: {group_name}')
            else:
                self.stdout.write(f'\n⚠️  Group already exists: {group_name}')
                group.permissions.clear()

            # Assign regular permissions
            assigned_count = 0
            for perm_string in config['permissions']:
                try:
                    app_label, codename = perm_string.split('.', 1)
                    permission = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename
                    )
                    group.permissions.add(permission)
                    assigned_count += 1
                except Permission.DoesNotExist:
                    self.stdout.write(f'  ❌ Permission not found: {perm_string}')
                except ValueError:
                    self.stdout.write(f'  ❌ Invalid permission format: {perm_string}')

            # Assign custom permissions
            custom_assigned = 0
            for perm_codename in config['custom_permissions']:
                try:
                    permission = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(permission)
                    custom_assigned += 1
                except Permission.DoesNotExist:
                    self.stdout.write(f'  ❌ Custom permission not found: {perm_codename}')

            self.stdout.write(f'  📊 Assigned {assigned_count} regular permissions')
            self.stdout.write(f'  📊 Assigned {custom_assigned} custom permissions')

    def print_summary(self):
        """Print a summary of created groups and permissions"""
        self.stdout.write('\n📊 SUMMARY:')
        self.stdout.write('=' * 50)

        total_groups = Group.objects.count()
        total_permissions = Permission.objects.count()

        self.stdout.write(f'Total groups: {total_groups}')
        self.stdout.write(f'Total permissions: {total_permissions}')

        self.stdout.write('\n👥 Available Groups:')
        for group in Group.objects.all().order_by('name'):
            perm_count = group.permissions.count()
            self.stdout.write(f'• {group.name}: {perm_count} permissions')
