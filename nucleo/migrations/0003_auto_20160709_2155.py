# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0002_auto_20160708_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missao',
            name='meta',
            field=models.IntegerField(verbose_name='meta em Reais (R$)'),
        ),
    ]