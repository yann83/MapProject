# floorproject/administrator/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Gestionnaire personnalisé pour notre modèle d'utilisateur
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, role='carte'):
        # Crée et enregistre un utilisateur avec le nom d'utilisateur et mot de passe donnés
        if not username:
            raise ValueError('Le nom d\'utilisateur est obligatoire')

        user = self.model(
            username=username,
            role=role,
        )
        user.set_password(password)  # Hache le mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        # Crée et enregistre un superutilisateur
        user = self.create_user(
            username=username,
            password=password,
            role='admin',
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Notre modèle d'utilisateur personnalisé
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('carte', 'Carte'),
        ('plan', 'Plan'),
        ('admin', 'Admin'),
    )

    username = models.CharField(max_length=30, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='carte')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  # Champ utilisé pour l'authentification

    def __str__(self):
        return self.username