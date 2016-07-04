# coding=utf-8
from __future__ import unicode_literals

from django.db import models

class Pagamento(models.Model):

    STATUS_DISPONIVEL = 0

    STATUS_CHOICES = [
        (STATUS_DISPONIVEL, 'disponível'),
    ]

    valor = models.FloatField()
    status = models.IntegerField(choices=STATUS_CHOICES)

    def __unicode__(self):
        return self.valor