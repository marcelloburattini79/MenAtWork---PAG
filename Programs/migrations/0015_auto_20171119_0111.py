# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-19 00:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Programs', '0014_auto_20171118_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='note',
            field=models.TextField(blank=None, default=None, null=True, verbose_name='Note'),
        ),
    ]
