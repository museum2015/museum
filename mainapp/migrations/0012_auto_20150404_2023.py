# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20150311_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributeassignment',
            name='actual',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='condition_descr',
            field=models.CharField(max_length=2000, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attributeassignment',
            name='attr_value',
            field=models.CharField(default=b'None', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='_class',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='aim_of_receiving_gen',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='amount',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='author',
            field=models.CharField(default=b'', max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='circumst_write_off',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='collection',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='condition',
            field=models.CharField(default=b'', max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='description',
            field=models.TextField(default=b'', max_length=1000, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='identifier',
            field=models.CharField(default=b'', max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='image',
            field=models.ImageField(default=b'default.jpg', null=True, upload_to=mainapp.models.get_image_path),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='is_there',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='mark_on_object',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='material',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='name',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='note',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='place_appellation',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='price',
            field=models.CharField(default=b'', max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='reason',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='recomm_for_restauration',
            field=models.CharField(default=b'', max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='restauration_notes',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='size',
            field=models.CharField(default=b'', max_length=40, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='source',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='storage',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='technique',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='term_back',
            field=models.DateTimeField(default=b'2000-02-12 00:00', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='transferred_from',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='transferred_to',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='type',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='way_of_found',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
    ]
