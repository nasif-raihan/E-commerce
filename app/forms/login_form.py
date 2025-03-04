from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from django.utils.translation import gettext_lazy


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True})
    )
    password = forms.CharField(
        strip=False,
        label=gettext_lazy("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "auto-complete": "current-password"},
        ),
    )
