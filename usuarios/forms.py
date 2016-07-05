# coding=utf-8
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import Usuario

class CadastroFrom(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
    c_password = forms.CharField(label='Confirme sua senha', widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'password']

    def clean(self):
        cleaned_data = super(CadastroFrom, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('c_password'):
            self.add_error('password', 'Senhas não conferem')
            self.add_error('c_password', '')
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.CharField(label='E-mail', widget=forms.EmailInput())
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())

    _usuario = None

    @property
    def usuario(self):
        return self._usuario

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        self._usuario = authenticate(email=cleaned_data.get('email'), password=cleaned_data.get('password'))
        if not self._usuario:
            self.add_error('email', '')
            self.add_error('password', '')
            raise ValidationError('E-mail e/ou senha incorretos')
        return cleaned_data

class AlterarFotoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['foto']