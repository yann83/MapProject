# floorproject/administrator/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles=[]):
    """
    Decorator that checks if the user has one of the allowed roles.
    Parameters:
    allowed_roles: List of allowed roles ('admin', 'map', 'plan')
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if user is logged in
            if not request.user.is_authenticated:
                return redirect('login')

            # Check if the user's role is in the list of allowed roles
            if request.user.role in allowed_roles or request.user.role == 'admin':
                # Admin has access to everything, or user has an authorized role
                return view_func(request, *args, **kwargs)
            else:
                # Add an error message
                messages.error(request, "You do not have the necessary permissions to access this page..")
                # Redirect to home page
                return redirect('administrator-index')

        return _wrapped_view

    return decorator