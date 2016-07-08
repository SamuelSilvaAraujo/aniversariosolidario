# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-08 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='status',
            field=models.IntegerField(choices=[(0, 'aguardando pagamento'), (1, 'dispon\xedvel')], default=0),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='valor',
            field=models.IntegerField(),
        ),
    ]
