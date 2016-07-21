# coding=utf-8
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.staticfiles.templatetags.staticfiles import static
from easy_thumbnails.files import get_thumbnailer
from ordered_model.models import OrderedModel

from financeiro.models import Pagamento
from usuarios.models import Usuario

class Missao(models.Model):
    usuario = models.ForeignKey(Usuario)
    titulo = models.CharField('título', max_length=255)
    beneficiado = models.CharField('beneficiado', max_length=255)
    descricao = models.TextField('descrição')
    slug = models.SlugField('slug', blank=True, max_length=255)
    meta = models.IntegerField('meta em Reais (R$)')

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

    @property
    def foto_divulgacao_quadrada_url(self):
        medias = self.medias.all()
        if not medias:
            return static('imgs/no-photo-aniversario.png')
        media = medias.first()
        return get_thumbnailer(media.arquivo).get_thumbnail({
            'size': (360, 270),
            'crop': True
        }).url

@receiver(pre_save, sender=Missao)
def pre_save_Missao(instance, **kwargs):
    if not instance.slug:
        instance.gerar_slug()

class Feedback(models.Model):
    mensagem = models.TextField('Mensagem aos doadores')
    opniao = models.TextField('Opnião sobre serviço')

    def __unicode__(self):
        return self.mensagem

class Aniversario(models.Model):
    class Meta:
        unique_together = ('usuario', 'ano')

    usuario = models.ForeignKey(Usuario, related_name='aniversarios')
    missao = models.ForeignKey(Missao)
    ano = models.IntegerField('Ano')
    apelo = models.TextField('apelo', blank=True)
    finalizado = models.DateTimeField(null=True, blank=True)
    feeback_liberado = models.BooleanField(default=False)
    feedblack = models.ForeignKey(Feedback, null=True, blank=True)

    def __unicode__(self):
        return 'Aniversário de {} - {}'.format(self.usuario.nome, self.missao.titulo)

    @property
    def usuario_proximo_aniversario(self):
        return self.usuario.proximo_aniversario.replace(year=self.ano)

    @property
    def full_url(self):
        return '{}{}'.format(settings.FULL_URL, reverse('aniversario:index', kwargs={
            'slug_usuario': self.usuario.slug,
            'slug_missao': self.missao.slug
        }))

    def dias_restantes(self):
        if self.usuario.proximo_aniversario < datetime.date.today():
            return 0
        return self.usuario.calcular_dias_restantes_proximo_aniversario(self.ano)

    @property
    def restam_para_aniversario_completo(self):
        restam = []
        if not self.apelo:
            restam += [{
                'field': 'apelo',
                'col': -1
            }]
        if not self.missao.medias.all():
            restam += [{
                'field': 'medias',
                'col': -1
            }]
        if not self.usuario.foto:
            restam += [{
                'field': 'usuario-foto',
                'col': -1
            }]

        for i in range(len(restam)):
            restam[i]['col'] = 12/len(restam)

        return restam

    @property
    def meta_atingida(self):
        return self.doacoes.pagas().aggregate(
            Sum('pagamento__valor')
        ).get('pagamento__valor__sum') or 0

    @property
    def meta_atingida_por(self):
        return int((float(self.meta_atingida) / self.missao.meta) * 100)

    @property
    def meta_de_direito(self):
        return (self.doacoes.pagas().aggregate(
            Sum('pagamento__valor')
        ).get('pagamento__valor__sum', 0) or 0)*(1-settings.TAXA)

    @property
    def meta_de_direito_disponivel(self):
        return (self.doacoes.filter(
            pagamento__status__in=['disponivel']
        ).aggregate(
            Sum('pagamento__valor')
        ).get('pagamento__valor__sum') or 0)*(1-settings.TAXA)

class DoacaoManager(models.Manager):
    def pagas(self):
        return super(DoacaoManager, self).get_queryset().filter(
            pagamento__status__in=['pago', 'disponivel']
        )

class Doacao(models.Model):
    class Meta:
        ordering = ['-data']

    usuario = models.ForeignKey(Usuario, related_name='doacoes_feitas')
    aniversario = models.ForeignKey(Aniversario, related_name='doacoes')
    pagamento = models.ForeignKey(Pagamento)
    data = models.DateTimeField(auto_now_add=True)

    objects = DoacaoManager()

    def __unicode__(self):
        return 'Doação para o Aniversário Solidário de {}: {}'.format(self.usuario.nome, self.aniversario.missao.titulo)

class MediaManager(models.Manager):
    def exceto_primeiro(self):
        return self.all()[1:]

class Media(OrderedModel):
    class Meta(OrderedModel.Meta):
        pass

    order_with_respect_to = 'missao'

    descricao = models.CharField('Descrição', max_length=140, blank=True)
    missao = models.ForeignKey(Missao, related_name='medias')
    arquivo = models.FileField()

    objects = MediaManager()

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

    @property
    def empty_fields(self):
        r = []
        if not self.data_de_nascimento:
            r += ['data_de_nascimento']
        return r

    @property
    def arquivo_folder_url(self):
        return get_thumbnailer(self.arquivo).get_thumbnail({
            'size': (960, 400),
            'crop': True,
            'upscale': True
        }).url

    DM_DICT = {
        'lg': (480, 480),
        'md': (240, 240),
        'sm': (120, 120),
        'xs': (60, 60)
    }

    def get_arquivo_url(self, dm):
        return get_thumbnailer(self.arquivo).get_thumbnail({
            'size': Usuario.DM_DICT.get(dm),
            'upscale': True
        }).url

    @property
    def arquivo_lg_url(self):
        return self.get_arquivo_url('lg')

    @property
    def arquivo_md_url(self):
        return self.get_arquivo_url('md')

    @property
    def arquivo_sm_url(self):
        return self.get_arquivo_url('sm')

    @property
    def arquivo_xs_url(self):
        return self.get_arquivo_url('xs')