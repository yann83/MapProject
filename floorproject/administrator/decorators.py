# floorproject/administrator/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles=[]):
    """
    Décorateur qui vérifie si l'utilisateur a l'un des rôles autorisés
    Paramètres:
        allowed_roles: Liste des rôles autorisés ('admin', 'carte', 'plan')
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Vérifier si l'utilisateur est connecté
            if not request.user.is_authenticated:
                return redirect('login')

            # Vérifier si le rôle de l'utilisateur est dans la liste des rôles autorisés
            if request.user.role in allowed_roles or request.user.role == 'admin':
                # Admin a accès à tout, ou l'utilisateur a un rôle autorisé
                return view_func(request, *args, **kwargs)
            else:
                # Ajouter un message d'erreur
                messages.error(request, "Vous n'avez pas les permissions nécessaires pour accéder à cette page.")
                # Rediriger vers la page d'accueil
                return redirect('administrator-index')

        return _wrapped_view

    return decorator