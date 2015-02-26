# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collection', models.CharField(max_length=200)),
                ('name_title', models.CharField(max_length=200)),
                ('name_lang', models.CharField(max_length=200)),
                ('name_type', models.CharField(max_length=200)),
                ('is_fragment', models.BooleanField(default=False)),
                ('amount', models.IntegerField(default=0)),
                ('size_type', models.CharField(max_length=200)),
                ('size_number', models.IntegerField(default=0)),
                ('size_measurement_unit', models.CharField(max_length=200)),
                ('_class', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('material', models.CharField(max_length=200)),
                ('technique', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=1000)),
                ('description_lang', models.CharField(max_length=50)),
                ('description_type', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
