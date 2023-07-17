from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    privacy = forms.BooleanField(label=_('Ich habe die Datenschutzerklärung gelesen und stimme ihr zu.'))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

