# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_remove_object_approval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='price',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
    ]
