# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-07 05:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webserver', '0002_pessoa_esta_desaparecido'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='encoding_distance_to_zero',
            field=models.FloatField(blank=True, null=True),
        ),
    ]