# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='status',
            field=models.CharField(choices=[('aguardando', 'Aguardando'), ('em_analise', 'Em an\xe1lise'), ('pago', 'Pago'), ('disponivel', 'Dispon\xedvel'), ('em_disputa', 'Em disputa'), ('devolvido', 'Devolvido'), ('cancelado', 'Cancelado')], default='aguardando', max_length=32),
        ),
    ]
