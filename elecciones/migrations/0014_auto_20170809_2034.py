# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 23:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elecciones', '0013_remove_lugarvotacion_geo'),
    ]

    operations = [
        migrations.AddField(
            model_name='opcion',
            name='obligatorio',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='votomesaoficial',
            name='votos',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='votomesareportado',
            name='votos',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
