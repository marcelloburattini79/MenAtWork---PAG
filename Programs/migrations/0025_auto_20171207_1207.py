# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-07 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Programs', '0024_auto_20171120_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='ordineServizio',
            field=models.FileField(blank=True, default=None, null=True, upload_to='ordineServizio', verbose_name='Ordine di servizio'),
        ),
        migrations.AddField(
            model_name='task',
            name='pianoCampionamento',
            field=models.FileField(blank=True, default=None, null=True, upload_to='pianiCampionamento', verbose_name='Piani di campionamento'),
        ),
        migrations.AlterField(
            model_name='task',
            name='offerta',
            field=models.FileField(blank=True, default=None, null=True, upload_to='offerte', verbose_name='Offerta'),
        ),
        migrations.AlterField(
            model_name='task',
            name='tecnici',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='taskAssegnati', to='Programs.Tecnico', verbose_name='Tecnici'),
        ),
    ]