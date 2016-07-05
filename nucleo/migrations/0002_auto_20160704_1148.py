# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-04 11:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nucleo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='doacao',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doacoes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='aniversario',
            name='missao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Missao'),
        ),
        migrations.AddField(
            model_name='aniversario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aniversarios', to=settings.AUTH_USER_MODEL),
        ),
    ]