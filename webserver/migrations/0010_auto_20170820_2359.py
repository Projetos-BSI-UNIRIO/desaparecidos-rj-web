# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-21 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webserver', '0009_auto_20170807_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='cor_olhos',
            field=models.CharField(blank=True, choices=[('azuis', 'Azuis'), ('castanhos_claros', 'Castanhos Claros'), ('castanhos_escuros', 'Castanhos Escuros'), ('cinzentos', 'Cinzentos'), ('castanhos', 'Castanhos'), ('desiguais_na_cor', 'Desiguais na Cor'), ('pretos', 'Pretos'), ('verdes', 'Verdes'), ('violetas', 'Violetas')], max_length=100, null=True),
        ),
    ]
