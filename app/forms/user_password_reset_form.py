from django import forms
from django.contrib.auth.forms import PasswordResetForm

from django.utils.translation import gettext_lazy


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=gettext_lazy("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "autocomplete": "email"}
        ),
    )
