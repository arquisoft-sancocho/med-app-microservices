#!/bin/bash
# Django commands to setup permissions
# Run this from the Django project directory

echo 'Setting up medical system permissions...'

# Run the custom management command
python manage.py setup_permissions

echo 'Permissions setup completed!'

# Verify groups were created
echo 'Created groups:'
python manage.py shell -c "from django.contrib.auth.models import Group; print(f'Administradores: {Group.objects.filter(name='Administradores').exists()}')"
python manage.py shell -c "from django.contrib.auth.models import Group; print(f'Medicos: {Group.objects.filter(name='Medicos').exists()}')"
python manage.py shell -c "from django.contrib.auth.models import Group; print(f'Enfermeros: {Group.objects.filter(name='Enfermeros').exists()}')"
python manage.py shell -c "from django.contrib.auth.models import Group; print(f'Recepcionistas: {Group.objects.filter(name='Recepcionistas').exists()}')"
python manage.py shell -c "from django.contrib.auth.models import Group; print(f'Tecnicos_Laboratorio: {Group.objects.filter(name='Tecnicos_Laboratorio').exists()}')"
python manage.py shell -c "from django.contrib.auth.models import Group; print(f'Auditores_Medicos: {Group.objects.filter(name='Auditores_Medicos').exists()}')"
python manage.py shell -c "from django.contrib.auth.models import Group; print(f'Farmaceuticos: {Group.objects.filter(name='Farmaceuticos').exists()}')"