# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 11:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0014_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AlterField(
            model_name='doacao',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doacoes_feitas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='doacao',
            name='doador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doacoes_feitas', to='nucleo.Doador'),
        ),
    ]
