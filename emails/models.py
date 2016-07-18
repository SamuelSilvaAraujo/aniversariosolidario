# coding=utf-8
from __future__ import unicode_literals

import random
import string

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template import loader
from django.utils import timezone
from mailer import Mailer, Message


class ContaDeEmail(models.Model):
    @staticmethod
    def get_naoresponda():
        return ContaDeEmail.objects.filter(responsabilidade=ContaDeEmail.NAO_RESPONDA).order_by('?').first()

    class Meta:
        verbose_name = 'conta de e-mail'
        verbose_name_plural = 'contas de e-mail'

    NAO_RESPONDA = 0
    CONTATO = 1

    RESPONSABILIDADE_CHOICES = [
        (NAO_RESPONDA, 'não reponda'),
        (CONTATO, 'contato'),
    ]

    responsabilidade = models.IntegerField('responsabilidade', choices=RESPONSABILIDADE_CHOICES)
    servidor = models.CharField('servidor', max_length=256)
    porta = models.IntegerField('porta')
    usuario = models.CharField('usuário', max_length=128)
    senha = models.CharField('senha', max_length=128)
    tls = models.BooleanField('TLS?', default=False)
    ssl = models.BooleanField('SSL?', default=False)
    campo_email = models.EmailField('e-mail', blank=True)

    def __unicode__(self):
        return 'Conta de E-mail - {}'.format(self.verbose())

    def verbose(self):
        return '{}: {} [{}:{}]'.format(
            self.responsabilidade_verbose,
            self.usuario,
            self.servidor,
            self.porta
        )

    @property
    def email(self):
        return self.campo_email if self.campo_email else self.usuario

    @property
    def responsabilidade_verbose(self):
        return dict(ContaDeEmail.RESPONSABILIDADE_CHOICES).get(self.responsabilidade)

    @property
    def mailer(self):
        return Mailer(
            host=self.servidor,
            port=int(self.porta),
            use_tls=self.tls,
            use_ssl=self.ssl,
            usr=self.usuario,
            pwd=self.senha,
        )

    def enviar(self, email):
        message = Message(
            From=self.email,
            to=email.para_email,
            charset='utf-8',
            # TODO: List-Unsubscribe
            # headers={'List-Unsubscribe': '<{}{}>'.format(
            #     settings.FULL_URL,
            #     reverse('unsubscribe_email', kwargs={'chave': self.emailconfig.chave})
            # )}
        )
        message.Subject = email.assunto
        message.Body = email.corpo
        if email.corpo_html:
            message.Html = email.corpo_html
        self.mailer.send(message)
        email.enviado = timezone.now()
        email.save(update_fields=['enviado'])

    def test(self):
        try:
            message = Message(
                From=self.email,
                to='douglas.paz.net@gmail.com',
                charset='utf-8',
            )
            message.Subject = 'Testando...'
            message.Body = '... tudo OK'
            self.mailer.send(message)
        except:
            return False
        return True

class ConfiguracaoDeEmail(models.Model):
    chave = models.CharField('chave', max_length=4)
    email = models.EmailField('e-mail')
    cancelado_as = models.DateTimeField('cancelado às..', null=True, blank=True)

    def gerar_chave(self):
        while not self.chave or ConfiguracaoDeEmail.objects.filter(chave=self.chave):
            self.chave = ''.join(map(lambda x: random.choice(string.uppercase), range(4)))
        return self.chave

@receiver(pre_save, sender=ConfiguracaoDeEmail)
def pre_save_ConfiguracaoDeEmail(instance, **kwargs):
    if not instance.chave:
        instance.gerar_chave()

class Email(models.Model):
    @staticmethod
    def normalize_email(email):
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    class Meta:
        verbose_name = 'e-mail'
        verbose_name_plural = 'e-mails'

    chave = models.CharField('chave', max_length=8, blank=True)
    de = models.ForeignKey(ContaDeEmail, related_name='emails')
    para_email = models.EmailField('e-mail')
    assunto = models.CharField('assunto', max_length=255)
    corpo = models.TextField('corpo')
    corpo_html = models.TextField('corpo HTML', blank=True)
    enviar_as = models.DateTimeField('enviar às', null=True)
    processado = models.DateTimeField('processado às..', null=True)
    enviado = models.DateTimeField('enviado às..', null=True)

    def __unicode__(self):
        return 'E-mail {} para {} - {}'.format(
            'enviado' if self.enviado else 'não enviado',
            self.para_email,
            self.assunto
        )

    def gerar_chave(self):
        while not self.chave or Email.objects.filter(chave=self.chave):
            self.chave = ''.join(map(lambda x: random.choice(string.uppercase), range(0, 8)))
        return self.chave

    @property
    def para(self):
        get, create = ConfiguracaoDeEmail.objects.get_or_create(email=self.para_email)
        return get

    def processar(self):
        if self.enviar_as and self.enviar_as < timezone.now():
            self.processado = timezone.now()
            self.save(update_fields=['processado'])
            if not self.para.cancelado_as:
                self.de.enviar(self)

    def carregar_corpo(self, template_txt, template_html=None, save=True, **kwargs):
        unsubscribe_url = '{}{}'.format(settings.FULL_URL, reverse('cancelar_envio_de_emails', kwargs={'chave': self.para.chave}))
        self.corpo = loader.render_to_string(template_txt, kwargs)
        self.corpo += loader.render_to_string('emails/txt_footer.txt', {
            'unsubscribe_url': unsubscribe_url
        })
        if template_html:
            kwargs.update({
                'unsubscribe_url': unsubscribe_url
            })
            self.corpo_html = loader.render_to_string(template_html, kwargs)
        if save:
            self.save(update_fields=['corpo', 'corpo_html'])
        return

@receiver(pre_save, sender=Email)
def pre_save_Email(instance, **kwargs):
    if not instance.chave:
        instance.gerar_chave()

@receiver(post_save, sender=Email)
def post_save_Email(instance, created, **kwargs):
    if created and instance.para:
        pass