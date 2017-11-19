# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-19 00:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Programs', '0018_auto_20171119_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='oraArrivo',
            field=models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Ora di arrivo'),
        ),
        migrations.AlterField(
            model_name='task',
            name='tecnici',
            field=models.ManyToManyField(blank=True, related_name='taskAssegnati', to='Programs.Tecnico', verbose_name='Tecnici'),
        ),
    ]
