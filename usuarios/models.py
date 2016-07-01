# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify


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
    data_ativacao_email = models.DateTimeField('data de ativação do e-mail', null=True)
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

@receiver(pre_save, sender=Usuario)
def pre_save_Usuario(instance, **kwargs):
    if not instance.slug:
        instance.gerar_slug()