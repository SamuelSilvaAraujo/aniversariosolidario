# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 16:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financeiro', '0005_pagamento_boleto_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lagradouro', models.TextField()),
                ('numero', models.IntegerField(verbose_name='n\xfamero')),
                ('complemento', models.TextField()),
                ('bairro', models.CharField(max_length=64)),
                ('estado', models.CharField(max_length=2)),
                ('cep', models.CharField(max_length=8)),
                ('cidade', models.CharField(max_length=64)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enderecos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]