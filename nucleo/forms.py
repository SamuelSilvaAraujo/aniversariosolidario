# coding=utf-8
from django import forms
from .models import Missao,Media

from aniversariosolidario import settings

import magic

class MissaoForm(forms.ModelForm):
    class Meta:
        model = Missao
        fields = ['titulo', 'descricao', 'meta']


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