# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20150513_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='reason',
            field=models.FileField(default=b'default.txt', null=True, upload_to=b''),
            preserve_default=True,
        ),
    ]
