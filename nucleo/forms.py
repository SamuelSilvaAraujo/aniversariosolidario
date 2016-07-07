# coding=utf-8
from django import forms
from .models import Missao,Media

from aniversariosolidario import settings

import magic

class MissaoForm(forms.ModelForm):
    titulo = forms.CharField(label='Qual a causa social?')
    beneficiado = forms.CharField(label='Nome do Beneficiado', help_text='Nome da instituição, grupo ou nome da pessoa que será beneficiada')

    class Meta:
        model = Missao
        fields = ['titulo', 'beneficiado', 'descricao', 'meta']


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['arquivo','descricao']

    def clean(self):
        cleaned_data = super(MediaForm,self).clean()
        f = magic.Magic(mime=True, uncompress=True)
        if not f.from_buffer(cleaned_data.get('arquivo').read()) in settings.MEDIA_TYPES:
            self.add_error('arquivo', 'Arquivo não permitido!')
        return cleaned_data