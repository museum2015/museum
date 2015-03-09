# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20150309_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='note_type',
        ),
    ]
