from __future__ import unicode_literals

from django.db import models
from ordered_model.models import OrderedModel
from financeiro.models import Pagamento

class Missao(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    slug = models.SlugField(blank=True,max_length=255)

class Aniversario(models.Model):
    missao = models.ForeignKey(Missao)
    ano = models.IntegerField()

class Doacao(models.Model):
    aniversario = models.ForeignKey(Aniversario)
    pagamento = models.ForeignKey(Pagamento)

class Media(OrderedModel):

    class Meta(OrderedModel.Meta):
        pass

    missao = models.ForeignKey(Missao)
    arquivo = models.FileField()