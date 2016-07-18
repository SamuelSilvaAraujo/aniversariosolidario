# coding=utf-8
from __future__ import unicode_literals

import random
import string
import datetime

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from easy_thumbnails.files import get_thumbnailer
from emails.models import Email, ContaDeEmail


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
    data_de_nascimento = models.DateField('data de nascimento', null=True, blank=True)
    foto = models.ImageField('foto', null=True, blank=True)
    e_equipe = models.BooleanField('é da equipe?', default=False)
    data_ativacao_email = models.DateTimeField('data de ativação do e-mail', null=True, blank=True)
    data_cadastro = models.DateTimeField('data de cadastro', auto_now_add=True)
    email_pagseguro = models.EmailField('e-mail PagSeguro', blank=True, null= True)

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
            'crop': True,
            'upscale': True
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

    @property
    def empty_fields(self):
        r = []
        if not self.data_de_nascimento:
            r += ['data_de_nascimento']
        return r

    @property
    def proximo_aniversario(self):
        if not self.data_de_nascimento:
            return None
        proximo = self.data_de_nascimento.replace(year=datetime.date.today().year)
        if proximo < datetime.date.today():
            proximo = proximo.replace(year=datetime.date.today().year+1)
        return proximo

    @property
    def aniversario_solidario(self):
        if not self.proximo_aniversario:
            return None
        from nucleo.models import Aniversario
        return Aniversario.objects.filter(
            usuario=self,
            ano__in=[self.proximo_aniversario.year, self.proximo_aniversario.year-1],
            finalizado__isnull=True
        ).first()

    @property
    def aniversarios_passados(self):
        return self.aniversarios.filter(usuario=self, finalizado__isnull=False)

    @property
    def dias_restantes_proximo_aniversario(self):
        return self.calcular_dias_restantes_proximo_aniversario()

    def calcular_dias_restantes_proximo_aniversario(self, ano=datetime.date.today().year):
        return (self.proximo_aniversario - datetime.date.today().replace(year=ano)).days

@receiver(pre_save, sender=Usuario)
def pre_save_Usuario(instance, **kwargs):
    if not instance.slug:
        instance.gerar_slug()

@receiver(post_save, sender=Usuario)
def post_save_Usuario(instance, created, **kwargs):
    if created and not instance.data_ativacao_email:
        ConfirmacaoDeEmail.objects.create(usuario=instance)

class ConfirmacaoDeEmail(models.Model):
    class Meta:
        ordering = ['data_solicitacao']

    usuario = models.ForeignKey(Usuario, related_name='confirmacoes_de_email')
    chave = models.CharField('chave', max_length=16, blank=True, unique=True)
    data_solicitacao = models.DateTimeField('data de solicitação', auto_now_add=True)
    email = models.ForeignKey(Email, null=True, blank=True, related_name='confirmacoes_de_email', on_delete=models.SET_NULL)

    def __unicode__(self):
        return 'Chave de ativação de {}'.format(self.usuario)

    def gerar_chave(self):
        while True:
            self.chave = ''.join(map(lambda x: random.choice(string.ascii_uppercase), range(16)))
            if not ConfirmacaoDeEmail.objects.filter(chave=self.chave):
                break
        return True

    def enviar_email(self):
        email = Email.objects.create(
            de=ContaDeEmail.get_naoresponda(),
            para_email=self.usuario.email,
            assunto='Confirme seu e-mail'
        )
        email.carregar_corpo(
            'usuarios/emails/confirmar_email.txt',
            'usuarios/emails/confirmar_email.html',
            url_de_confirmacao='{}{}'.format(
                settings.FULL_URL,
                reverse('usuarios:confirmar_email', kwargs={'chave': self.chave})
            )
        )
        email.enviar_as = timezone.now()
        email.save(update_fields=['enviar_as'])
        self.email = email
        self.save(update_fields=['email'])

@receiver(pre_save, sender=ConfirmacaoDeEmail)
def pre_save_ConfirmacaoDeEmail(instance, **kwargs):
    if not instance.chave:
        instance.gerar_chave()

@receiver(post_save, sender=ConfirmacaoDeEmail)
def post_save_ConfirmacaoDeEmail(instance, **kwargs):
    if not instance.email:
        instance.enviar_email()

class RecuperarSenha(models.Model):
    chave = models.CharField('chave', max_length=16, blank=True, unique=True)
    usuario = models.ForeignKey(Usuario, related_name='recuperacoes_de_senha')
    email = models.ForeignKey(Email, related_name='recuperacaoes_de_senha', null=True, blank=True, on_delete=models.SET_NULL)

    def gerar_chave(self):
        while True:
            self.chave = ''.join(map(lambda x: random.choice(string.ascii_uppercase), range(16)))
            if not RecuperarSenha.objects.filter(chave=self.chave):
                break
        return True

    def enviar_email(self):
        email = Email.objects.create(
            de=ContaDeEmail.get_naoresponda(),
            para_email=self.usuario.email,
            assunto='Redefina sua senha'
        )
        email.carregar_corpo(
            'usuarios/emails/recuperar_senha.txt',
            'usuarios/emails/recuperar_senha.html',
            url_para_redefinir='{}{}'.format(
                settings.FULL_URL,
                reverse('usuarios:recuperarsenha:confirmar', kwargs={'chave': self.chave})
            )
        )
        email.enviar_as = timezone.now()
        email.save(update_fields=['enviar_as'])
        self.email = email
        self.save(update_fields=['email'])

@receiver(pre_save, sender=RecuperarSenha)
def pre_save_RecuperarSenha(instance, **Kwargs):
    if not instance.chave:
        instance.gerar_chave()

@receiver(post_save, sender=RecuperarSenha)
def post_save_RecuperarSenha(instance, **kwargs):
    if not instance.email:
        instance.enviar_email()