# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-03-05 20:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adjuntos', '0007_auto_20190305_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='mesa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='elecciones.Mesa'),
        ),
    ]
