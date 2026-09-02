from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)
from django.contrib.auth.models import User

from .models import Profile


class RegistrationForm(UserCreationForm):
    """Form used to register a new user."""

    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email


class ProfileForm(forms.ModelForm):
    """Form used to update a user's profile."""

    class Meta:
        model = Profile
        fields = [
            "profile_picture",
            "bio",
        ]


class UserUpdateForm(forms.ModelForm):
    """Form used to update basic user information."""

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(
            email=email
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email