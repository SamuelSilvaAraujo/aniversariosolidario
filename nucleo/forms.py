# coding=utf-8
from django import forms
from .models import Missao,Media, Aniversario, Feedback

from aniversariosolidario import settings

import magic

class MissaoForm(forms.ModelForm):
    titulo = forms.CharField(label='Qual a causa social?')
    beneficiado = forms.CharField(label='Nome do Beneficiado', help_text='Nome da instituição, grupo ou nome da pessoa que será beneficiada')

    class Meta:
        model = Missao
        fields = ['titulo', 'beneficiado', 'descricao', 'meta']


class MediaForm(forms.ModelForm):
    arquivo = forms.FileField(label='Selecione uma imagem')

    class Meta:
        model = Media
        fields = ['arquivo', 'descricao']

    def clean(self):
        cleaned_data = super(MediaForm,self).clean()
        f = magic.Magic(mime=True, uncompress=True)
        if not cleaned_data.get('arquivo'):
            self.add_error('arquivo', 'Escolha um arquivo antes de enviar!')
        else:
            if not f.from_buffer(cleaned_data.get('arquivo').read()) in settings.MEDIA_TYPES:
                self.add_error('arquivo', 'Arquivo não permitido!')
        return cleaned_data

class MediaEditarForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['descricao']

class AniversarioApeloForm(forms.ModelForm):
    apelo = forms.CharField(label='Escreva uma mensagem para os seus amigos', widget=forms.Textarea())

    class Meta:
        model = Aniversario
        fields = ['apelo']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['mensagem', 'opniao']