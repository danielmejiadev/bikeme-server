# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-08 20:39
from __future__ import unicode_literals

import Apps.BikeMe.models.user_model
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('uid', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('typeChallenge', models.IntegerField()),
                ('condition', models.IntegerField()),
                ('award', models.IntegerField()),
            ],
            options={
                'ordering': ('typeChallenge',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
            ],
            options={
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(default=0)),
                ('date', models.CharField(max_length=100)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guests', to='BikeMe.Event')),
            ],
            options={
                'ordering': ('event',),
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
                'ordering': ('route', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calification', models.FloatField()),
                ('recommendation', models.FloatField()),
                ('date', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('route',),
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
                ('distance', models.FloatField()),
                ('level', models.IntegerField()),
                ('image', models.TextField()),
                ('departure', models.TextField()),
                ('arrival', models.TextField()),
                ('created', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('displayName', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('level', models.IntegerField(default=0)),
                ('photo', models.TextField(default='')),
                ('aboutMe', models.TextField(default='')),
                ('socialNetworks', models.TextField(default='{}')),
                ('preferenceDays', models.CharField(default='[]', max_length=100)),
                ('preferenceHours', models.CharField(default='[]', max_length=100)),
                ('achievements', models.TextField(default='[]')),
                ('updated', models.CharField(default=Apps.BikeMe.models.user_model.getCurrentDate, max_length=100)),
                ('created', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('uid', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('durationSeconds', models.IntegerField()),
                ('beginDate', models.CharField(max_length=100)),
                ('comment', models.TextField(default='')),
                ('routeLatLngList', models.TextField()),
                ('totalDistanceMeters', models.IntegerField()),
                ('averageSpeedKm', models.IntegerField()),
                ('averageAltitudeMeters', models.IntegerField()),
                ('typeRoute', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workouts', to='BikeMe.User')),
            ],
            options={
                'ordering': ('beginDate',),
            },
        ),
        migrations.AddField(
            model_name='route',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_routes', to='BikeMe.User'),
        ),
        migrations.AddField(
            model_name='rating',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='BikeMe.Route'),
        ),
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='BikeMe.User'),
        ),
        migrations.AddField(
            model_name='point',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='BikeMe.Route'),
        ),
        migrations.AddField(
            model_name='guest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='BikeMe.User'),
        ),
        migrations.AddField(
            model_name='event',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='BikeMe.Route'),
        ),
    ]
