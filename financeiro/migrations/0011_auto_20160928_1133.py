# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-28 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0010_auto_20160803_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='valor',
            field=models.FloatField(),
        ),
    ]
