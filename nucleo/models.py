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
    titulo = models.CharField('título', max_length=255)
    beneficiado = models.CharField('beneficiado', max_length=255)
    descricao = models.TextField('descrição')
    slug = models.SlugField('slug', blank=True, max_length=255)
    meta = models.FloatField('meta em Reais (R$)')

    def __unicode__(self):
        return self.titulo

    def gerar_slug(self):
        tentativa = 0
        while not self.slug or Missao.objects.filter(slug=self.slug):
            if tentativa > 0:
                self.slug = '{}-{}'.format(
                    slugify(self.titulo),
                    tentativa
                )
            else:
                self.slug = slugify(self.titulo)
            tentativa += 1
        return True


@receiver(pre_save, sender=Missao)
def pre_save_Missao(instance, **kwargs):
    if not instance.slug:
        instance.gerar_slug()

class Aniversario(models.Model):
    class Meta:
        unique_together = ('usuario', 'ano')

    usuario = models.ForeignKey(Usuario, related_name='aniversarios')
    missao = models.ForeignKey(Missao)
    ano = models.IntegerField('Ano')
    apelo = models.TextField('apelo', blank=True)

    def __unicode__(self):
        return self.usuario.nome

    @property
    def usuario_proximo_aniversario(self):
        return self.usuario.proximo_aniversario.replace(year=self.ano)

class Doacao(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='doacoes')
    aniversario = models.ForeignKey(Aniversario)
    pagamento = models.ForeignKey(Pagamento)
    data = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.usuario.nome

class Media(OrderedModel):

    class Meta(OrderedModel.Meta):
        pass

    order_with_respect_to = 'missao'

    descricao = models.CharField('Descrição', max_length=140, blank=True)
    missao = models.ForeignKey(Missao, related_name='medias')
    arquivo = models.FileField()

    def __unicode__(self):
        return self.descricao

    _editar_form = None
    def editar_form(self, *args, **kwargs):
        from nucleo.forms import MediaEditarForm
        self._editar_form = MediaEditarForm(*args, instance=self, prefix='media_{}'.format(self.id), **kwargs)
        return self._editar_form

    @property
    def get_editar_form(self):
        return self._editar_form if self._editar_form else self.editar_form()