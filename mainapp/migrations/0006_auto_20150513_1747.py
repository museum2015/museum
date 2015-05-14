# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20150513_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='image',
            field=models.ImageField(default=b'default.jpg', upload_to=b'/images/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='reason',
            field=models.FileField(default=b'default.txt', null=True, upload_to=b'/docs/'),
            preserve_default=True,
        ),
    ]
