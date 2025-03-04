from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm

from django.utils.translation import gettext_lazy


class SetUserPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        strip=False,
        label=gettext_lazy("New Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "new-password"}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        label=gettext_lazy("Confirm New Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "new-password"}
        ),
    )
