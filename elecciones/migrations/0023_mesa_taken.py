# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-15 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elecciones', '0022_auto_20171014_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='mesa',
            name='taken',
            field=models.DateTimeField(null=True),
        ),
    ]
