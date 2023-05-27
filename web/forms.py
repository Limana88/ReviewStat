from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    name_company = forms.CharField()

    class Meta:
        model = User
        fields = ('email', 'password', 'name_company')


class AuthForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
