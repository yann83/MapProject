# floorproject/administrator/forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import CustomUser

class UserCreationForm(forms.ModelForm):
    """Form to create a new user with a password"""
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmation du mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'role')

    def clean_password2(self):
        # Check that the two passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas")
        return password2

    def save(self, commit=True):
        # Saves the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """Form to update a user"""
    password = ReadOnlyPasswordHashField(
        label="Mot de passe",
        help_text=(
            "Les mots de passe ne sont pas stockés en clair, donc il n'y a pas moyen "
            "de voir le mot de passe de cet utilisateur, mais vous pouvez le changer "
            "en utilisant <a href=\"../password/\">ce formulaire</a>."
        ),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'role', 'is_active')