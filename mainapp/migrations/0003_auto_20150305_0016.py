# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20150305_0006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='size_measurement_unit',
        ),
        migrations.AlterField(
            model_name='object',
            name='size_number',
            field=models.CharField(default=b'', max_length=40),
            preserve_default=True,
        ),
    ]
