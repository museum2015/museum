# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20150307_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='author_type',
        ),
        migrations.RemoveField(
            model_name='object',
            name='description_lang',
        ),
        migrations.RemoveField(
            model_name='object',
            name='description_type',
        ),
        migrations.RemoveField(
            model_name='object',
            name='image_type',
        ),
        migrations.RemoveField(
            model_name='object',
            name='mark_note_lang',
        ),
        migrations.RemoveField(
            model_name='object',
            name='mark_type',
        ),
        migrations.RemoveField(
            model_name='object',
            name='name_lang',
        ),
        migrations.RemoveField(
            model_name='object',
            name='name_type',
        ),
        migrations.RemoveField(
            model_name='object',
            name='price_type',
        ),
        migrations.AlterField(
            model_name='attributeassignment',
            name='attr_value',
            field=models.CharField(default=b'null', max_length=200),
            preserve_default=True,
        ),
    ]
