# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-13 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='email_pagseguro',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='e-mail PagSeguro'),
        ),
    ]
