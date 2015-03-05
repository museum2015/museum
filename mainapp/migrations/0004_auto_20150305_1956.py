# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20150305_0016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='object',
            old_name='name_title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='object',
            old_name='size_number',
            new_name='size',
        ),
        migrations.RenameField(
            model_name='object',
            old_name='place',
            new_name='storage',
        ),
        migrations.RemoveField(
            model_name='object',
            name='size_type',
        ),
        migrations.AddField(
            model_name='attributeassignment',
            name='approval',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='approval',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
