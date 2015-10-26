# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measurement',
            old_name='measurement_type',
            new_name='type',
        ),
        migrations.AlterUniqueTogether(
            name='measurement',
            unique_together=set([('datetime', 'type', 'sensor_id')]),
        ),
    ]
