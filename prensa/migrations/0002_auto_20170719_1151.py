# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prensa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='relacion',
            field=models.CharField(blank=True, choices=[('AMIGX', 'AMIGX'), ('COMPAÑERX', 'COMPAÑERX'), ('INDIFERENTE', 'INDIFERENTE'), ('OPOSITXR', 'OPOSITXR')], max_length=20),
        ),
    ]