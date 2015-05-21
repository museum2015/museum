# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20150515_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='_class',
        ),
        migrations.AddField(
            model_name='activity',
            name='aim',
            field=models.ForeignKey(to='mainapp.Object', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='classify',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='stat',
            field=models.CharField(default=b'\xd0\x9f\xd1\x83\xd1\x81\xd1\x82\xd0\xb8\xd0\xb9 \xd0\xbe\xd0\xb1\xe2\x80\x99\xd1\x94\xd0\xba\xd1\x82', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='approval',
            field=models.NullBooleanField(default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=models.CharField(max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='aim_of_receiving_gen',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='amount',
            field=models.IntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='author',
            field=models.CharField(default=b'', max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='bibliography',
            field=models.CharField(default=b'', max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='circumst_write_off',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='condition',
            field=models.CharField(default=b'', max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='condition_descr',
            field=models.CharField(max_length=2000, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='date_creation',
            field=models.CharField(default=b'', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='date_detection',
            field=models.CharField(default=b'', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='date_existence',
            field=models.CharField(default=b'', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='description',
            field=models.TextField(default=b'', max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='identifier',
            field=models.CharField(default=b'', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='is_there',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='link_on_doc',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='mark_on_object',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='material',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='memorial_subject',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='name',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='note',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='place_appellation',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='place_detection',
            field=models.CharField(default=b'', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='place_existence',
            field=models.CharField(default=b'', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='place_of_creation',
            field=models.CharField(default=b'', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='price',
            field=models.CharField(default=b'', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='recomm_for_restauration',
            field=models.CharField(default=b'', max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='restauration_notes',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='side_1',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='side_2',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='size',
            field=models.CharField(default=b'', max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='storage',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='technique',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='term_back',
            field=models.DateField(default=b'2000-01-01', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='type',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='way_of_found',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
