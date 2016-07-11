# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from pagseguro.models import Checkout, TRANSACTION_STATUS_CHOICES


class Pagamento(models.Model):
    valor = models.IntegerField()
    status = models.CharField(choices=TRANSACTION_STATUS_CHOICES, default='aguardando', max_length=32)
    checkout = models.ForeignKey(Checkout, related_name='pagamentos', null=True)