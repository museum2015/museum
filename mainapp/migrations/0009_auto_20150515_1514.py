# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20150514_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='image',
            field=models.ImageField(default=b'default.jpg', null=True, upload_to=b'images/'),
            preserve_default=True,
        ),
    ]
