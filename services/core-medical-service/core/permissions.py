"""
Permission utilities for the medical system.
Contains decorators and helper functions for managing permissions.
"""

from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.core.exceptions import PermissionDenied


def user_in_group(group_name):
    """Check if user belongs to a specific group"""
    def check_group(user):
        return user.groups.filter(name=group_name).exists() if user.is_authenticated else False
    return check_group


def user_has_permission(permission_name):
    """Check if user has a specific permission"""
    def check_permission(user):
        return user.has_perm(permission_name) if user.is_authenticated else False
    return check_permission


def can_access_examenes(user):
    """Check if user can access examenes"""
    if not user.is_authenticated:
        return False
    
    allowed_groups = ['Administrador', 'Medico', 'Medico_de_Junta', 'Enfermero', 'Tecnico']
    return user.groups.filter(name__in=allowed_groups).exists() or user.has_perm('can_view_all_examenes')


def can_access_diagnosticos(user):
    """Check if user can access diagnosticos"""
    if not user.is_authenticated:
        return False
    
    allowed_groups = ['Administrador', 'Medico', 'Medico_de_Junta', 'Enfermero', 'Tecnico']
    return user.groups.filter(name__in=allowed_groups).exists() or user.has_perm('can_view_all_diagnosticos')


def can_access_cirugias(user):
    """Check if user can access cirugias"""
    if not user.is_authenticated:
        return False
    
    # Solo Administrador, Medico y Medico_de_Junta pueden ver cirugias
    allowed_groups = ['Administrador', 'Medico', 'Medico_de_Junta']
    return user.groups.filter(name__in=allowed_groups).exists() or user.has_perm('can_view_all_cirugias')


def can_access_consultas(user):
    """Check if user can access consultas"""
    if not user.is_authenticated:
        return False
    
    # Solo Administrador, Medico, Medico_de_Junta y Enfermero pueden ver consultas
    allowed_groups = ['Administrador', 'Medico', 'Medico_de_Junta', 'Enfermero']
    return user.groups.filter(name__in=allowed_groups).exists() or user.has_perm('can_view_all_consultas')


def can_add_examenes(user):
    """Check if user can add examenes"""
    if not user.is_authenticated:
        return False
    
    allowed_groups = ['Administrador', 'Medico', 'Medico_de_Junta', 'Enfermero', 'Tecnico']
    return user.groups.filter(name__in=allowed_groups).exists() or user.has_perm('can_add_examenes')


def can_add_diagnosticos(user):
    """Check if user can add diagnosticos"""
    if not user.is_authenticated:
        return False
    
    allowed_groups = ['Administrador', 'Medico', 'Medico_de_Junta', 'Enfermero']
    return user.groups.filter(name__in=allowed_groups).exists() or user.has_perm('can_add_diagnosticos')


def can_add_cirugias(user):
    """Check if user can add cirugias"""
    if not user.is_authenticated:
        return False
    
    # Solo Administrador, Medico y Medico_de_Junta pueden agregar cirugias
    allowed_groups = ['Administrador', 'Medico', 'Medico_de_Junta']
    return user.groups.filter(name__in=allowed_groups).exists() or user.has_perm('can_add_cirugias')


def can_add_consultas(user):
    """Check if user can add consultas"""
    if not user.is_authenticated:
        return False
    
    # Solo Administrador, Medico, Medico_de_Junta y Enfermero pueden agregar consultas
    allowed_groups = ['Administrador', 'Medico', 'Medico_de_Junta', 'Enfermero']
    return user.groups.filter(name__in=allowed_groups).exists() or user.has_perm('can_add_consultas')


# Decoradores para vistas
def require_examenes_access(view_func):
    """Decorator to require examenes access"""
    @wraps(view_func)
    @login_required
    @user_passes_test(can_access_examenes, login_url='/permission-denied/')
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def require_diagnosticos_access(view_func):
    """Decorator to require diagnosticos access"""
    @wraps(view_func)
    @login_required
    @user_passes_test(can_access_diagnosticos, login_url='/permission-denied/')
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def require_cirugias_access(view_func):
    """Decorator to require cirugias access"""
    @wraps(view_func)
    @login_required
    @user_passes_test(can_access_cirugias, login_url='/permission-denied/')
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def require_consultas_access(view_func):
    """Decorator to require consultas access"""
    @wraps(view_func)
    @login_required
    @user_passes_test(can_access_consultas, login_url='/permission-denied/')
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def require_add_permission(permission_check_func):
    """Generic decorator for add permissions"""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        @user_passes_test(permission_check_func, login_url='/permission-denied/')
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# Mixins para Class-Based Views
class ExamenesAccessMixin(UserPassesTestMixin):
    """Mixin for examenes access in CBVs"""
    def test_func(self):
        return can_access_examenes(self.request.user)


class DiagnosticosAccessMixin(UserPassesTestMixin):
    """Mixin for diagnosticos access in CBVs"""
    def test_func(self):
        return can_access_diagnosticos(self.request.user)


class CirugiasAccessMixin(UserPassesTestMixin):
    """Mixin for cirugias access in CBVs"""
    def test_func(self):
        return can_access_cirugias(self.request.user)


class ConsultasAccessMixin(UserPassesTestMixin):
    """Mixin for consultas access in CBVs"""
    def test_func(self):
        return can_access_consultas(self.request.user)


class AddExamenesPermissionMixin(UserPassesTestMixin):
    """Mixin for add examenes permission in CBVs"""
    def test_func(self):
        return can_add_examenes(self.request.user)


class AddDiagnosticosPermissionMixin(UserPassesTestMixin):
    """Mixin for add diagnosticos permission in CBVs"""
    def test_func(self):
        return can_add_diagnosticos(self.request.user)


class AddCirugiasPermissionMixin(UserPassesTestMixin):
    """Mixin for add cirugias permission in CBVs"""
    def test_func(self):
        return can_add_cirugias(self.request.user)


class AddConsultasPermissionMixin(UserPassesTestMixin):
    """Mixin for add consultas permission in CBVs"""
    def test_func(self):
        return can_add_consultas(self.request.user)


def get_user_permissions_context(user):
    """Get user permissions context for templates"""
    if not user.is_authenticated:
        return {
            'can_access_examenes': False,
            'can_access_diagnosticos': False,
            'can_access_cirugias': False,
            'can_access_consultas': False,
            'can_add_examenes': False,
            'can_add_diagnosticos': False,
            'can_add_cirugias': False,
            'can_add_consultas': False,
            'user_groups': [],
            'is_admin': False,
            'is_medico': False,
            'is_enfermero': False,
            'is_tecnico': False,
        }
    
    user_groups = list(user.groups.values_list('name', flat=True))
    
    return {
        'can_access_examenes': can_access_examenes(user),
        'can_access_diagnosticos': can_access_diagnosticos(user),
        'can_access_cirugias': can_access_cirugias(user),
        'can_access_consultas': can_access_consultas(user),
        'can_add_examenes': can_add_examenes(user),
        'can_add_diagnosticos': can_add_diagnosticos(user),
        'can_add_cirugias': can_add_cirugias(user),
        'can_add_consultas': can_add_consultas(user),
        'user_groups': user_groups,
        'is_admin': 'Administrador' in user_groups,
        'is_medico': 'Medico' in user_groups or 'Medico_de_Junta' in user_groups,
        'is_enfermero': 'Enfermero' in user_groups,
        'is_tecnico': 'Tecnico' in user_groups,
    }
