# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-18 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Programs', '0013_auto_20171118_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='note',
            field=models.TextField(blank='', default=None, null=True, verbose_name='Note'),
        ),
    ]
