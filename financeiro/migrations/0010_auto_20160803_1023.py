# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-03 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0009_transacao_taxa_atual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='aniversario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transacoes', to='nucleo.Aniversario'),
        ),
    ]
