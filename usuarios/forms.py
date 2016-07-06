# coding=utf-8
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import Usuario,RecuperarSenha

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
    foto = forms.ImageField(label='Selecione um arquivo')

    class Meta:
        model = Usuario
        fields = ['foto']

class AlterarPerfilForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['nome', 'data_de_nascimento']

class CompletarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = []

    def __init__(self, fields, *args, **kwargs):
        super(CompletarPerfilForm, self).__init__(*args, **kwargs)
        for field in fields:
            if field == 'data_de_nascimento':
                self.fields[field] = forms.DateTimeField(label='Qual a data do seu aniversário?', widget=forms.TextInput(attrs={'placeholder': '31/12/19XX'}))
                self.Meta.fields.append(field)


class EditarSenhaForm(forms.Form):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
    c_password = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(EditarSenhaForm, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('c_password'):
            self.add_error('password', 'Senhas não conferem')
            self.add_error('c_password', '')
        return cleaned_data

class RecuperarSenhaForm(forms.Form):
    email = forms.CharField(label='Qual o e-mail vinculado a sua conta?', widget=forms.EmailInput())

    _usuario = None

    @property
    def usuario(self):
        return self._usuario

    def clean(self):
        cleaned_data = super(RecuperarSenhaForm, self).clean()
        self._usuario = Usuario.objects.filter(email = cleaned_data.get('email')).first()
        if not self._usuario:
            self.add_error('email', 'Não existe nenhum usuário cadastrado com esse e-mail!')
        return cleaned_data