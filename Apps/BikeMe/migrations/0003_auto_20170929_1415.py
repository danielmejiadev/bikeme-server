# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-29 19:15
from __future__ import unicode_literals

import Apps.BikeMe.bikemeutils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BikeMe', '0002_auto_20170910_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='updated',
            field=models.CharField(default=Apps.BikeMe.bikemeutils.BikeMeUtils.getCurrentDate, max_length=100),
        ),
    ]
