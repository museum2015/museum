# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20150305_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='approval',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
