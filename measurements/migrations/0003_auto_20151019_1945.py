# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0002_auto_20151019_1524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measurement',
            old_name='val_si',
            new_name='val_converted',
        ),
    ]
