# floorproject/administrator/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    # Forms for adding and editing user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # Fields to display in the administration interface
    list_display = ('username', 'role', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'role')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Rôle', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    # Only add these fields when creating a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

# Register the custom user model with the Django admin
admin.site.register(CustomUser, UserAdmin)