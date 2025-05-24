# floorproject/administrator/forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import CustomUser

class UserCreationForm(forms.ModelForm):
    """Form to create a new user with a password"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'role')

    def clean_password2(self):
        # Check that the two passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
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
        label="Password",
        help_text=(
            "Passwords are not stored in clear text, so there is no way to "
            "see this user's password, but you can change it using "
            "<a href=\"../password/\">this form</a>."
        ),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'role', 'is_active')