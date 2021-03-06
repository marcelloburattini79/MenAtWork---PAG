# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-19 00:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Programs', '0016_auto_20171119_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='offerta',
            field=models.FileField(blank=True, null=True, upload_to='offerte', verbose_name='Offerta'),
        ),
        migrations.AlterField(
            model_name='task',
            name='oraArrivo',
            field=models.CharField(blank=True, max_length=500, verbose_name='Ora di arrivo'),
        ),
        migrations.AlterField(
            model_name='task',
            name='tecnici',
            field=models.ManyToManyField(blank=True, related_name='taskAssegnati', to='Programs.Tecnico', verbose_name='Tecnici'),
        ),
    ]
