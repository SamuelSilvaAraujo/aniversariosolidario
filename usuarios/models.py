# coding=utf-8
from __future__ import unicode_literals

import random
import string

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from easy_thumbnails.files import get_thumbnailer


class UsuarioManager(BaseUserManager):
    def _create_user(self, password, is_superuser, **kwargs):
        kwargs.update({
            'is_superuser': is_superuser
        })
        usuario = self.model(**kwargs)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_user(self, password, is_superuser, **kwargs):
        return self._create_user(password, is_superuser, **kwargs)

    def create_superuser(self, password, **kwargs):
        kwargs.update({
            'e_equipe': True,
            'data_ativacao_email': timezone.now()
        })
        return self._create_user(password, True, **kwargs)

class Usuario(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    email = models.EmailField('e-mail', unique=True)
    nome = models.CharField('nome', max_length=128)
    slug = models.SlugField('slug do nome', max_length=255, blank=True)
    data_de_nascimento = models.DateTimeField('data de nascimento', null=True, blank=True)
    foto = models.ImageField('foto', null=True, blank=True)
    e_senha_randomica = models.BooleanField('a senha ainda é randomica?', default=False)
    e_equipe = models.BooleanField('é da equipe?', default=False)
    data_ativacao_email = models.DateTimeField('data de ativação do e-mail', null=True, blank=True)
    data_cadastro = models.DateTimeField('data de cadastro', auto_now_add=True)

    objects = UsuarioManager()

    def __unicode__(self):
        return 'Usuário {} <{}>'.format(
            self.nome,
            self.email
        )

    @property
    def is_active(self):
        return True if self.data_ativacao_email else False

    @property
    def is_staff(self):
        return self.e_equipe

    def get_short_name(self):
        return self.nome.split(' ')[0]

    @property
    def nome_curto(self):
        nome_split = self.nome.split(' ')
        if len(nome_split) == 1:
            return nome_split[0]
        return ' '.join([nome_split[0], nome_split[-1]])

    def gerar_slug(self):
        tentativa = 0
        while not self.slug or Usuario.objects.filter(slug=self.slug):
            if tentativa > 0:
                self.slug = '{}-{}'.format(
                    slugify(self.nome_curto),
                    tentativa
                )
            else:
                self.slug = slugify(self.nome_curto)
            tentativa += 1
        return True

    DM_DICT = {
        'lg': (480, 480),
        'md': (240, 240),
        'sm': (120, 120),
        'xs': (60, 60)
    }

    def get_foto_url(self, dm):
        if not self.foto:
            return static('imgs/avatar-{}.png'.format(dm))
        return get_thumbnailer(self.foto).get_thumbnail({
            'size': Usuario.DM_DICT.get(dm),
            'crop': True
        }).url

    @property
    def foto_lg_url(self):
        return self.get_foto_url('lg')

    @property
    def foto_md_url(self):
        return self.get_foto_url('md')

    @property
    def foto_sm_url(self):
        return self.get_foto_url('sm')

    @property
    def foto_xs_url(self):
        return self.get_foto_url('xs')

@receiver(pre_save, sender=Usuario)
def pre_save_Usuario(instance, **kwargs):
    if not instance.slug:
        instance.gerar_slug()

class ConfirmacaoDeEmail(models.Model):
    class Meta:
        ordering = ['data_solicitacao']

    usuario = models.ForeignKey(Usuario, related_name='confirmacoes_de_email')
    chave = models.CharField('chave', max_length=16, blank=True, unique=True)
    data_solicitacao = models.DateTimeField('data de solicitação', auto_now_add=True)

    def __unicode__(self):
        return 'Chave de ativação de {}'.format(self.usuario)

    def gerar_chave(self):
        while True:
            self.chave = ''.join(map(lambda x: random.choice(string.ascii_uppercase), range(16)))
            if not ConfirmacaoDeEmail.objects.filter(chave=self.chave):
                break
        return True

@receiver(pre_save, sender=ConfirmacaoDeEmail)
def pre_save_ConfirmacaoDeEmail(instance, **kwargs):
    if not instance.chave:
        instance.gerar_chave()
    #TODO: enviar e-mail