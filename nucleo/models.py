# coding=utf-8
from __future__ import unicode_literals

import datetime
import urllib
from tempfile import mkstemp

import flickrapi
import os

from PIL import Image
from PIL.ImageDraw import ImageDraw, Draw
from PIL.ImageFont import ImageFont, truetype
from django.conf import settings
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.staticfiles.templatetags.staticfiles import static
from easy_thumbnails.files import get_thumbnailer
from emails.models import ContaDeEmail, Email
from ordered_model.models import OrderedModel

from financeiro.models import Pagamento
from usuarios.models import Usuario
from pagseguro.settings import PAYMENT_URL

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
    feedback = models.ForeignKey(Feedback, null=True, blank=True)
    imagem_divulgacao_fb = models.ImageField(null=True, blank=True)

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

    def enviar_email_iniciado(self):
        email = Email.objects.create(
            de=ContaDeEmail.get_naoresponda(),
            para_email=self.usuario.email,
            assunto='Aniversário Solidário de {} iniciado'.format(self.ano)
        )
        email.carregar_corpo(
            'nucleo/emails/aniversario_iniciado.txt',
            'nucleo/emails/aniversario_iniciado.html',
            ano=self.ano,
            aniversario_full_url=self.full_url
        )
        email.enviar_as = timezone.now()
        email.save(update_fields=['enviar_as'])

    DIVULGACAO_FB_SIZE = (1200, 630)
    def gerar_imagem_divulgacao_fb(self):
        delete_background = False
        try:
            background_path = get_thumbnailer(self.missao.medias.all()[0].arquivo).get_thumbnail({
                'size': Aniversario.DIVULGACAO_FB_SIZE,
                'crop': True,
                'upscale': True
            }).path
        except:
            flickr = flickrapi.FlickrAPI(settings.FLICKR_KEY, settings.FLICKR_SECRET_KEY)
            img_url = None
            filename = None
            for photo in flickr.walk(
                    tags=','.join(filter(lambda x: len(x) > 2, self.missao.beneficiado.split(' '))),
                    content_type=1
            ):
                img_url = 'http://farm{}.staticflickr.com/{}/{}_{}.jpg'.format(
                    photo.get('farm'),
                    photo.get('server'),
                    photo.get('id'),
                    photo.get('secret')
                )
                filename = '{}_{}.jpg'.format(
                    photo.get('id'),
                    photo.get('secret')
                )
                break
            i, temp_path = mkstemp(filename)
            urllib.urlretrieve(img_url, temp_path)
            im = Image.open(temp_path)
            w, h = im.size
            w_r = Aniversario.DIVULGACAO_FB_SIZE[0]/float(w)
            h_r = Aniversario.DIVULGACAO_FB_SIZE[1]/float(h)
            r = w_r if w_r > h_r else h_r
            im = im.resize((int(w*r), int(h*r)), Image.ANTIALIAS)
            background = Image.new('RGBA', Aniversario.DIVULGACAO_FB_SIZE, (255, 255, 255, 0))
            background.paste(
                im, (
                    (Aniversario.DIVULGACAO_FB_SIZE[0] - im.size[0]),
                    (Aniversario.DIVULGACAO_FB_SIZE[1] - im.size[1])
                )
            )
            background.save(temp_path)
            background_path = temp_path
            delete_background = True

        if background_path:
            background = Image.open(background_path, 'r').convert('RGBA')
            avatar = Image.open(self.usuario.get_foto_path('sm'), 'r').convert('RGBA')
            tarxa = Image.new('RGBA', (1200, 120), (236, 240, 241, 255))
            background.paste(tarxa, (0, 500))
            background.paste(avatar, (10, 500))
            txt = Image.new('RGBA', background.size, (255, 255, 255, 0))
            fnt = truetype(os.path.join(settings.STATIC_ROOT, 'fonts/fontastique.ttf'), 40)
            subfnt = truetype(os.path.join(settings.STATIC_ROOT, 'fonts/fontastique.ttf'), 30)
            draw = Draw(txt)
            draw.text((150, 520), self.usuario.nome_curto, font=fnt, fill=(44, 62, 80, 255))
            draw.text((150, 570), self.missao.titulo, font=subfnt, fill=(52, 73, 94, 255))
            final_img = Image.alpha_composite(background, txt)
            filename = '{}-fb-cover.png'.format(self.usuario.slug)
            i, temp_path = mkstemp(filename)
            final_img.save(temp_path)
            file = open(temp_path)
            django_file = File(file)
            self.imagem_divulgacao_fb.save(filename, django_file)
            file.close()
            os.unlink(temp_path)
            if delete_background: os.unlink(background_path)
            return True
        return False

    def get_imagem_divulgacao_fb_url(self):
        if not self.imagem_divulgacao_fb:
            self.gerar_imagem_divulgacao_fb()
        return '{}{}'.format(
            settings.MEDIA_FULL_URL,
            self.imagem_divulgacao_fb.name[2:]
        )


@receiver(post_save, sender=Aniversario)
def post_save_Aniversario(instance, created, **kwargs):
    if created:
        instance.enviar_email_iniciado()

class DoacaoManager(models.Manager):
    def pagas(self):
        return self.filter(
            pagamento__status__in=['pago', 'disponivel']
        )

    def aguardando_pagamento(self):
        return self.filter(
            pagamento__status='aguardando'
        )

    def em_analise(self):
        return self.filter(
            pagamento__status='em_analise'
        )

    def canceladas(self):
        return self.filter(
            pagamento__status__in=['cancelado', 'devolvido', 'em_disputa']
        )

class Doador(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()

class Doacao(models.Model):
    class Meta:
        ordering = ['-data']

    usuario = models.ForeignKey(Usuario, related_name='doacoes_feitas', null=True, blank=True)
    doador = models.ForeignKey(Doador, related_name='doacoes_feitas', null=True, blank=True)
    aniversario = models.ForeignKey(Aniversario, related_name='doacoes')
    pagamento = models.ForeignKey(Pagamento, related_name='doacoes')
    data = models.DateTimeField(auto_now_add=True)

    objects = DoacaoManager()

    def __unicode__(self):
        return 'Doação de {} para o Aniversário Solidário de {}'.format(
            self.usuario_nome,
            self.aniversario.usuario.nome,
            self.aniversario.missao.titulo
        )

    @property
    def checkout_url(self):
        if not self.pagamento.checkout:
            return reverse('financeiro:doacao_pagamento:index', kwargs={'doacao_id': self.id})
        return '{}?code={}'.format(PAYMENT_URL, self.pagamento.checkout.code)

    @property
    def usuario_nome(self):
        if self.usuario:
            return self.usuario.nome
        if self.doador:
            return self.doador.nome
        return 'Doador não identificado'

    @property
    def usuario_foto_url(self):
        if self.usuario:
            return self.usuario.foto_micro_url
        return static('imgs/avatar-micro.png')

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
            'upscale': True,
            'crop': True
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