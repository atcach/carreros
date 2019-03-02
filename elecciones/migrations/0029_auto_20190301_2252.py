# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-03-02 01:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elecciones', '0028_auto_20171024_0051'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeccionDePonderacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField()),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='circuito',
            name='localidad_cabecera',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='seccion',
            name='numero',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='secciondeponderacion',
            name='seccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elecciones.Seccion'),
        ),
        migrations.AddField(
            model_name='circuito',
            name='seccion_de_ponderacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elecciones.SeccionDePonderacion'),
        ),
    ]
