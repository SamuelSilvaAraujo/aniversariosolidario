# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-26 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0016_auto_20160801_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='mensagem',
            field=models.TextField(verbose_name='mensagem'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='opniao',
            field=models.TextField(blank=True, verbose_name='opini\xe3o'),
        ),
    ]
