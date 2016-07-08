# coding=utf-8
from __future__ import unicode_literals

from django.db import models

class Pagamento(models.Model):
    STATUS_AGUARDANDO = 0
    STATUS_DISPONIVEL = 1

    STATUS_CHOICES = [
        (STATUS_AGUARDANDO, 'aguardando pagamento'),
        (STATUS_DISPONIVEL, 'disponível'),
    ]

    valor = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_AGUARDANDO)

    def __unicode__(self):
        return self.valor