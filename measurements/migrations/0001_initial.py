# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('loop_id', models.IntegerField(default=None, null=True, blank=True)),
                ('measurement_type', models.CharField(max_length=3)),
                ('units', models.CharField(default=None, max_length=3, null=True, blank=True)),
                ('sensor_id', models.CharField(max_length=4)),
                ('val', models.IntegerField()),
                ('val_si', models.FloatField(default=None, null=True, blank=True)),
            ],
        ),
    ]
