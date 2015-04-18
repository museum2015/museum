# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20150414_0901'),
    ]

    operations = [
        migrations.RenameField(
            model_name='object',
            old_name='transferred_from',
            new_name='side_1',
        ),
        migrations.RenameField(
            model_name='object',
            old_name='transferred_to',
            new_name='side_2',
        ),
        migrations.RemoveField(
            model_name='object',
            name='reason',
        ),
        migrations.RemoveField(
            model_name='object',
            name='source',
        ),
        migrations.AddField(
            model_name='object',
            name='bibliography',
            field=models.CharField(default=b'', max_length=1000, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='date_creation',
            field=models.CharField(default=b'', max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='date_detection',
            field=models.CharField(default=b'', max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='date_existence',
            field=models.CharField(default=b'', max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='link_on_doc',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='memorial_subject',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='place_detection',
            field=models.CharField(default=b'', max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='place_existence',
            field=models.CharField(default=b'', max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='place_of_creation',
            field=models.CharField(default=b'', max_length=50, null=True),
            preserve_default=True,
        ),
    ]
