from django import forms
from .models import Missao

class MissaoForm(forms.ModelForm):
    class Meta:
        model = Missao
        fields = ['titulo','descricao']