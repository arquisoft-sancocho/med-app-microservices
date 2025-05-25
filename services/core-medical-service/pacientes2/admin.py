from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group  # Import Group

# Register your models here.
from .models import Paciente2

# Unregister the default User admin before registering the custom one
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    # Remove the duplicate addition of 'groups' to fieldsets
    # fieldsets = BaseUserAdmin.fieldsets + (
    #     ('Grupos', {'fields': ('groups',)}),
    # )
    # Keep the modification for add_fieldsets (user creation form)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Grupos', {'fields': ('groups',)}),
    )
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'display_groups')
    list_filter = BaseUserAdmin.list_filter + ('groups',)

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    display_groups.short_description = 'Groups'


# Re-register UserAdmin
admin.site.register(User, UserAdmin)

# Optional: Register Group admin if you want fine-grained control over groups themselves
# from django.contrib.auth.admin import GroupAdmin
# admin.site.register(Group, GroupAdmin)

# Register Paciente2 model
admin.site.register(Paciente2)
