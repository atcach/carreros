# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 00:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Circuito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Eleccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LugarVotacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('barrio', models.CharField(blank=True, max_length=100)),
                ('ciudad', models.CharField(blank=True, max_length=100)),
                ('geo', models.CharField(blank=True, max_length=200)),
                ('calidad', models.CharField(blank=True, editable=False, help_text='calidad de la geolocalizacion', max_length=20)),
                ('electores', models.PositiveIntegerField()),
                ('latitud', models.DecimalField(decimal_places=7, max_digits=10, null=True)),
                ('longitud', models.DecimalField(decimal_places=7, max_digits=10, null=True)),
                ('circuito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elecciones.Circuito')),
            ],
        ),
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField()),
                ('url', models.URLField(blank=True, help_text='url al telegrama')),
                ('circuito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elecciones.Circuito')),
                ('lugar_votacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elecciones.LugarVotacion', verbose_name='Lugar de votacion')),
            ],
        ),
        migrations.CreateModel(
            name='Opcion',
            fields=[
                ('dne_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField()),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VotoMesaOficial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votos', models.IntegerField()),
                ('eleccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elecciones.Eleccion')),
                ('mesa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elecciones.Mesa')),
                ('opcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elecciones.Opcion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VotoMesaReportado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votos', models.IntegerField()),
                ('eleccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elecciones.Eleccion')),
                ('mesa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elecciones.Mesa')),
                ('opcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elecciones.Opcion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='opcion',
            name='partido',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elecciones.Partido'),
        ),
        migrations.AddField(
            model_name='eleccion',
            name='opciones',
            field=models.ManyToManyField(to='elecciones.Opcion'),
        ),
        migrations.AddField(
            model_name='circuito',
            name='seccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elecciones.Seccion'),
        ),
        migrations.AlterUniqueTogether(
            name='votomesareportado',
            unique_together=set([('eleccion', 'mesa', 'opcion')]),
        ),
        migrations.AlterUniqueTogether(
            name='votomesaoficial',
            unique_together=set([('eleccion', 'mesa', 'opcion')]),
        ),
    ]
