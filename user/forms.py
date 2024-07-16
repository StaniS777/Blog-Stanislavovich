from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm,
    UserChangeForm,
)

from user.models import Profile, User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]
    

class UpdateMyProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]


class LoginForm(AuthenticationForm):
    pass


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 
            "first_name",
            "last_name",
            'email',
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'status_profile',
        )