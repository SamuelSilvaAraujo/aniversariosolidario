# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from pagseguro.models import Checkout, TRANSACTION_STATUS_CHOICES
from pagseguro.signals import notificacao_recebida

class Pagamento(models.Model):
    valor = models.IntegerField()
    status = models.CharField(choices=TRANSACTION_STATUS_CHOICES, default='aguardando', max_length=32)
    checkout = models.ForeignKey(Checkout, related_name='pagamentos', null=True)

    @property
    def status_verbose(self):
        return dict(TRANSACTION_STATUS_CHOICES).get(self.status)

    @property
    def status_valido(self):
        return self.status in ['pago', 'disponivel']


def pagseguro_notificacao_recebida(sender, transaction, **kwargs):
    from nucleo.models import Doacao
    from pagseguro.models import Transaction

    transaction_instance = Transaction.objects.get(code=transaction.get('code'))
    doacao = Doacao.objects.get(id=int(transaction_instance.reference))
    doacao.pagamento.status = transaction_instance.status
    doacao.pagamento.save(update_fields=['status'])

notificacao_recebida.connect(pagseguro_notificacao_recebida)


class Transacao(models.Model):

    valor = models.IntegerField()
    aniversario = models.ForeignKey('nucleo.Aniversario', related_name='aniversario_transacao')
    data_solicitacao = models.DateTimeField('Data de solicitação',auto_now_add=True)
    data_realizacao = models.DateTimeField('Data de realização' ,null=True, blank=True)

    def __unicode__(self):
        return 'Transação solitada em {}'.format(self.data_solicitacao)