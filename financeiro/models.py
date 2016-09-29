# coding=utf-8
from __future__ import unicode_literals

import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from emails.models import ContaDeEmail
from emails.models import Email
from pagseguro.models import Checkout, TRANSACTION_STATUS_CHOICES
from pagseguro.signals import notificacao_recebida, update_transaction
from usuarios.models import Usuario


logger = logging.getLogger(__name__)


class Pagamento(models.Model):
    valor = models.IntegerField()
    status = models.CharField(choices=TRANSACTION_STATUS_CHOICES, default='aguardando', max_length=32)
    checkout = models.ForeignKey(Checkout, related_name='pagamentos', null=True, blank=True)
    boleto_link = models.URLField('Link para o boleto', blank=True)
    cartao = models.ForeignKey(Checkout, related_name='pagamentos_por_cartao', null=True, blank=True)

    def __unicode__(self):
        return 'Pagamento {} - {}'.format(
            ', '.join(map(lambda x: unicode(x), self.doacoes.all())),
            self.status_verbose
        )

    @property
    def status_verbose(self):
        return dict(TRANSACTION_STATUS_CHOICES).get(self.status)

    @property
    def status_valido(self):
        return self.status in ['pago', 'disponivel']

    def enviar_email_doacao_completa(self):
        for doacao in self.doacoes.all():
            email = Email.objects.create(
                de=ContaDeEmail.get_naoresponda(),
                para_email=doacao.aniversario.usuario.email,
                assunto='Doação de R${} recebida'.format(self.valor)
            )
            email.carregar_corpo(
                'financeiro/emails/doacao_completa.txt',
                'financeiro/emails/doacao_completa.html',
                nome=doacao.usuario_nome,
                valor=self.valor,
                beneficiado=doacao.aniversario.missao.beneficiado,
                url_painel='{}{}'.format(settings.FULL_URL, reverse('usuarios:index'))
            )
            email.enviar_as = timezone.now()
            email.save(update_fields=['enviar_as'])

@receiver(post_save, sender=Pagamento)
def post_save_Pagamento(instance, update_fields, **kwargs):
    if update_fields and 'status' in update_fields and instance.status == 'pago':
        instance.enviar_email_doacao_completa()

class Transacao(models.Model):
    valor = models.FloatField()
    aniversario = models.ForeignKey('nucleo.Aniversario', related_name='transacoes')
    data_solicitacao = models.DateTimeField('Data de solicitação',auto_now_add=True)
    data_realizacao = models.DateTimeField('Data de realização' ,null=True, blank=True)
    taxa_atual = models.FloatField(default=settings.TAXA)

    def __unicode__(self):
        return 'Transação solitada em {}'.format(self.data_solicitacao)

class Endereco(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='enderecos')
    lagradouro = models.TextField()
    numero = models.IntegerField('número')
    complemento = models.TextField()
    bairro = models.CharField(max_length=64)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=64)

    def __unicode__(self):
        return '{}, {}{} - {} [{}/{}]'.format(
            self.lagradouro,
            self.numero,
            ' ({})'.format(self.complemento) if self.complemento else '',
            self.bairro,
            self.cidade,
            self.estado
        )

    def pagseguro_serialize(self):
        return {
            'street': self.lagradouro,
            'number': self.numero,
            'complement': self.complemento,
            'district': self.bairro,
            'postal_code': self.cep,
            'city': self.cidade,
            'state': self.estado,
            'country': 'BRA'
        }

def pagseguro_notificacao_recebida(sender, transaction, **kwargs):
    from nucleo.models import Doacao
    from pagseguro.models import Transaction

    transaction_instance = Transaction.objects.get(code=transaction.get('code'))
    doacao = Doacao.objects.get(id=int(transaction_instance.reference))
    doacao.pagamento.status = transaction_instance.status
    doacao.pagamento.save(update_fields=['status'])
    if not doacao.usuario and not doacao.doador:
        email = transaction.get('sender').get('email')
        nome = transaction.get('sender').get('name')

        try:
            doacao.usuario = Usuario.objects.get(email=email)
            doacao.save(update_fields=['usuario'])
        except ObjectDoesNotExist:
            pass

        if not doacao.usuario:
            from nucleo.models import Doador
            
            doacao.doador, created = Doador.objects.get_or_create(
                nome=nome,
                email=email
            )
            doacao.save(update_fields=['doador'])

notificacao_recebida.connect(pagseguro_notificacao_recebida)