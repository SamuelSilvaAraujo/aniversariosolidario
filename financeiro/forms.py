# coding=utf-8

from django import forms

from financeiro.models import Transacao

class TransacaoForm(forms.ModelForm):
    class Meta:
        model= Transacao
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