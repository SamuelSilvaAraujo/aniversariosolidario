# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-02 01:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0008_auto_20160723_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacao',
            name='taxa_atual',
            field=models.FloatField(default=0.12),
        ),
    ]