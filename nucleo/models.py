# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from ordered_model.models import OrderedModel

from financeiro.models import Pagamento
from usuarios.models import Usuario

class Missao(models.Model):
    titulo = models.CharField('Titulo',max_length=255)
    descricao = models.TextField('Descrição')
    slug = models.SlugField('Slug do titulo',blank=True,max_length=255)

    def __unicode__(self):
        return self.titulo

    @property
    def titulo_curto(self):
        titulo_split = self.titulo.split(' ')
        if(len(titulo_split) == 1):
            return titulo_split[0]
        return ' '.join([titulo_split[0], titulo_split[-1]])

    def gerar_slug(self):
        tentativa = 0
        while not self.slug or Missao.objects.filter(slug=self.slug):
            if tentativa > 0:
                self.slug = '{}-{}'.format(
                    slugify(self.titulo_curto),
                    tentativa
                )
            else:
                self.slug = slugify(self.titulo_curto)
            tentativa += 1
        return True


@receiver(pre_save, sender=Missao)
def pre_save_Missao(instance, **kwargs):
    if not instance.slug:
        instance.gerar_slug()

class Aniversario(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='aniversarios')
    missao = models.ForeignKey(Missao)
    ano = models.IntegerField('Ano')

    def __unicode__(self):
        return self.usuario.nome

class Doacao(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='doacoes')
    aniversario = models.ForeignKey(Aniversario)
    pagamento = models.ForeignKey(Pagamento)

    def __unicode__(self):
        return self.usuario.nome

class Media(OrderedModel):

    class Meta(OrderedModel.Meta):
        pass

    descricao = models.CharField('Descrição', max_length=140)
    missao = models.ForeignKey(Missao)
    arquivo = models.FileField()

    def __unicode__(self):
        return self.descricao