# coding=utf-8

from django import forms
from django.core.exceptions import ValidationError

from financeiro.models import Transacao
from localflavor.br.forms import BRCPFField
from usuarios.models import Usuario


class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['valor']

    _aniversario = None

    def __init__(self, aniversario, *args, **kwargs):
        self._aniversario = aniversario
        super(TransacaoForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TransacaoForm, self).clean()
        meta_disponivel = self._aniversario.meta_de_direito_disponivel
        if cleaned_data.get('valor') > meta_disponivel:
            self.add_error('valor', 'você não tem direito a esse valor!')
        return cleaned_data

class UsuarioCompletoForm(forms.ModelForm):
    cpf = BRCPFField(label='Seu CPF', required=True)

    class Meta:
        model = Usuario
        fields = ['email', 'nome', 'cpf', 'telefone_ddd', 'telefone_numero']

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome.split(' ')) == 1:
            raise ValidationError('Utilize seu nome e sobrenome', code='invalid')
        return nome