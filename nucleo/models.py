# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from ordered_model.models import OrderedModel
from financeiro.models import Pagamento

class Missao(models.Model):
    titulo = models.CharField('Titulo',max_length=255)
    descricao = models.TextField('Descrição')
    slug = models.SlugField('Slug',blank=True,max_length=255)

    def __unicode__(self):
        return self.titulo

class Aniversario(models.Model):
    missao = models.ForeignKey(Missao)
    ano = models.IntegerField('Ano')

class Doacao(models.Model):
    aniversario = models.ForeignKey(Aniversario)
    pagamento = models.ForeignKey(Pagamento)

class Media(OrderedModel):

    class Meta(OrderedModel.Meta):
        pass

    missao = models.ForeignKey(Missao)
    arquivo = models.FileField()