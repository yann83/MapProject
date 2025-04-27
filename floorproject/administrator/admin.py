# floorproject/administrator/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    # Les formulaires pour ajouter et modifier des instances d'utilisateur
    form = UserChangeForm
    add_form = UserCreationForm

    # Les champs à afficher dans l'interface d'administration
    list_display = ('username', 'role', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'role')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Rôle', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    # Ajoute seulement ces champs lors de la création d'un utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

# Enregistre le modèle d'utilisateur personnalisé avec l'admin Django
admin.site.register(CustomUser, UserAdmin)