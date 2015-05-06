# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='date_creation',
            field=models.CharField(default=b'', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='object',
            name='date_detection',
            field=models.CharField(default=b'', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='object',
            name='date_existence',
            field=models.CharField(default=b'', max_length=50, null=True),
        ),
    ]
