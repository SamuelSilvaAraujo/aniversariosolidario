# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-24 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0011_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='aniversario',
            name='imagem_divulgacao_fb',
            field=models.ImageField(null=True, upload_to=b''),
        ),
    ]