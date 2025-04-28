# floorproject/administrator/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Custom handler for our user model
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, role='carte'):
        # Creates and registers a user with the given username and password
        if not username:
            raise ValueError('Username is required')

        user = self.model(
            username=username,
            role=role,
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        # Create and register a superuser
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


# Our custom user model
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

    USERNAME_FIELD = 'username'  # Field used for authentication

    def __str__(self):
        return self.username