"""
URL configuration for floorproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# floorproject/floorproject/urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from public.views import public_index, public_plans, public_cartes
from administrator.views import (administrator_index, administrator_cartes,
                                administrator_plans, administrator_edit_carte,
                                administrator_edit_plans, administrator_upload,
                                administrator_users, administrator_add_user,
                                administrator_edit_user, administrator_delete_user)

urlpatterns = [
    path('', public_index, name="index"),
    path('plans', public_plans, name="plans"),
    path('cartes', public_cartes, name="cartes"),
    path('login/', auth_views.LoginView.as_view(template_name='administrator/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/', template_name='administrator/logout.html'), name='logout'),
    path('administrator/', administrator_index, name="administrator-index"),
    path('administrator/cartes', administrator_cartes, name="administrator-cartes"),
    path('administrator/plans', administrator_plans, name="administrator-plans"),
    path('administrator/edit/carte', administrator_edit_carte, name="administrator-edit-carte"),
    path('administrator/edit/plans', administrator_edit_plans, name="administrator-edit-plans"),
    path('administrator/upload', administrator_upload, name="administrator-upload"),
    path('administrator/users/', administrator_users, name="administrator-users"),
    path('administrator/users/add/', administrator_add_user, name="administrator-add-user"),
    path('administrator/users/edit/<int:user_id>/', administrator_edit_user, name="administrator-edit-user"),
    path('administrator/users/delete/<int:user_id>/', administrator_delete_user, name="administrator-delete-user"),
    path('admin/', admin.site.urls),
]
