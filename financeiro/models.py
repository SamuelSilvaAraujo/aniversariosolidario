from __future__ import unicode_literals

from django.db import models

class Pagamento(models.Model):
    valor = models.FloatField()
    status = models.IntegerField()