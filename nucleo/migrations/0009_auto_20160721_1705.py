# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0008_aniversario_feeback_liberado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aniversario',
            old_name='feedblack',
            new_name='feedback',
        ),
        migrations.AlterField(
            model_name='aniversario',
            name='feeback_liberado',
            field=models.BooleanField(default=False),
        ),
    ]
