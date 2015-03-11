# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributeassignment',
            name='attr_value',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
