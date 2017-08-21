# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-07 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=254, null=True)),
                ('idade', models.IntegerField(blank=True, null=True)),
                ('altura', models.IntegerField(blank=True, null=True)),
                ('cor_pele', models.CharField(blank=True, choices=[('branca', 'Branca'), ('preta', 'Preta'), ('parda', 'Parda'), ('amarela', 'Amarela')], max_length=100, null=True)),
                ('cor_olhos', models.CharField(blank=True, choices=[('castanhos', 'Castanhos'), ('azuis', 'Azuis'), ('verdes', 'Verdes')], max_length=100, null=True)),
                ('cor_cabelos', models.CharField(blank=True, choices=[('preto', 'Castanhos'), ('loiro', 'Loiros'), ('ruivo', 'Ruivos')], max_length=100, null=True)),
                ('sexo', models.CharField(blank=True, choices=[('masculino', 'Masculino'), ('feminino', 'Feminino'), ('indeterminado', 'Indeterminado')], max_length=100, null=True)),
                ('nome_pai', models.CharField(blank=True, max_length=254, null=True)),
                ('nome_mae', models.CharField(blank=True, max_length=254, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos/')),
                ('facial_encoding', models.TextField(blank=True, null=True)),
                ('data_nascimento', models.DateTimeField(blank=True, null=True)),
                ('data_desaparecimento', models.DateTimeField(blank=True, null=True)),
                ('local_desaparecimento', models.CharField(blank=True, max_length=254, null=True)),
                ('cartazete', models.ImageField(blank=True, null=True, upload_to='cartazetes/')),
                ('nome_no_cartazete', models.CharField(blank=True, max_length=254, null=True)),
                ('comentario_desaparecimento', models.TextField(blank=True, null=True)),
                ('possui_tatuagem', models.BooleanField()),
                ('possui_cicatriz', models.BooleanField()),
                ('possui_deficiencia', models.BooleanField()),
                ('sofreu_amputacao', models.BooleanField()),
                ('tipo_fisico', models.CharField(blank=True, max_length=254, null=True)),
                ('rg', models.CharField(blank=True, max_length=9, null=True)),
                ('emissor_rg', models.CharField(blank=True, max_length=15, null=True)),
                ('cpf', models.CharField(blank=True, max_length=11, null=True)),
                ('cnh', models.CharField(blank=True, max_length=11, null=True)),
            ],
        ),
    ]
