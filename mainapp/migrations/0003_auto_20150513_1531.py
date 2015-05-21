# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20150428_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='image',
            field=models.ImageField(default=b'home/valeriy/photo0005.jpg', upload_to=mainapp.models.get_image_path),
            preserve_default=True,
        ),
    ]
