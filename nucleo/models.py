from __future__ import unicode_literals

from django.db import models
from ordered_model.models import OrderedModel

class Missao(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    slug = models.SlugField()

class Aniversario(models.Model):
    missao = models.ForeignKey(Missao)
    ano = models.DateField()

class Doacao(models.Model):
    aniversario = models.ForeignKey(Aniversario)

class Media(OrderedModel):

    class Meta(OrderedModel.Meta):
        pass

    missao = models.ForeignKey(Missao)
    arquivo = models.FileField()