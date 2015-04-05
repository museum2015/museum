# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mainapp.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_stamp', models.DateTimeField(default=b'2000-02-12 00:00')),
                ('type', models.CharField(max_length=30)),
                ('approval', models.BooleanField(default=False)),
                ('actor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttributeAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attr_name', models.CharField(max_length=40)),
                ('attr_value', models.CharField(default=b'None', max_length=200, null=True)),
                ('actual', models.BooleanField(default=False)),
                ('approval', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collection', models.CharField(default=b'', max_length=200, null=True)),
                ('is_fragment', models.BooleanField(default=False)),
                ('name', models.CharField(default=b'', max_length=200, null=True)),
                ('amount', models.IntegerField(default=0, null=True)),
                ('size', models.CharField(default=b'', max_length=40, null=True)),
                ('_class', models.CharField(default=b'', max_length=200, null=True)),
                ('type', models.CharField(default=b'', max_length=200, null=True)),
                ('material', models.CharField(default=b'', max_length=200, null=True)),
                ('technique', models.CharField(default=b'', max_length=200, null=True)),
                ('description', models.TextField(default=b'', max_length=1000, null=True)),
                ('identifier', models.CharField(default=b'', max_length=50, null=True)),
                ('image', models.ImageField(default=b'default.jpg', null=True, upload_to=mainapp.models.get_image_path)),
                ('author', models.CharField(default=b'', max_length=100, null=True)),
                ('price', models.CharField(default=b'', max_length=50, null=True)),
                ('mark_on_object', models.CharField(default=b'', max_length=200, null=True)),
                ('note', models.CharField(default=b'', max_length=200, null=True)),
                ('condition', models.CharField(default=b'', max_length=100, null=True)),
                ('condition_descr', models.CharField(max_length=2000, null=True)),
                ('transport_possibility', models.BooleanField(default=False)),
                ('recomm_for_restauration', models.CharField(default=b'', max_length=100, null=True)),
                ('restauration_notes', models.CharField(default=b'', max_length=200, null=True)),
                ('storage', models.CharField(default=b'', max_length=200, null=True)),
                ('place_appellation', models.CharField(default=b'', max_length=200, null=True)),
                ('is_there', models.CharField(default=b'', max_length=200, null=True)),
                ('way_of_found', models.CharField(default=b'', max_length=200, null=True)),
                ('transferred_from', models.CharField(default=b'', max_length=200, null=True)),
                ('transferred_to', models.CharField(default=b'', max_length=200, null=True)),
                ('term_back', models.DateTimeField(default=b'2000-02-12 00:00', max_length=200, null=True)),
                ('aim_of_receiving_gen', models.CharField(default=b'', max_length=200, null=True)),
                ('circumst_write_off', models.CharField(default=b'', max_length=200, null=True)),
                ('reason', models.CharField(default=b'', max_length=200, null=True)),
                ('source', models.CharField(default=b'', max_length=200, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='attributeassignment',
            name='aim',
            field=models.ForeignKey(to='mainapp.Object'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attributeassignment',
            name='event_initiator',
            field=models.ForeignKey(to='mainapp.Activity'),
            preserve_default=True,
        ),
    ]
