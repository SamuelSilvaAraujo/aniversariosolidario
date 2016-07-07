# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 18:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0006_auto_20160707_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='aniversario',
            name='apelo',
            field=models.TextField(blank=True, verbose_name='apelo'),
        ),
        migrations.AlterField(
            model_name='media',
            name='descricao',
            field=models.CharField(blank=True, max_length=140, verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='media',
            name='missao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medias', to='nucleo.Missao'),
        ),
    ]