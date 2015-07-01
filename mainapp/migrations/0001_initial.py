# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_stamp', models.DateTimeField(default=b'2000-02-12 00:00')),
                ('type', models.CharField(max_length=150)),
                ('approval', models.NullBooleanField(default=None)),
            ],
            options={
                'permissions': (('only_personal_activity', '\u0431\u0430\u0447\u0438\u0442\u0438 \u0442i\u043b\u044c\u043a\u0438 \u0441\u0432\u043ei'), ('all_activity', '\u0431\u0430\u0447\u0438\u0442\u0438 \u0432\u0441\u0435')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttributeAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attr_name', models.CharField(max_length=40)),
                ('attr_value', models.CharField(default=b'None', max_length=200, null=True)),
                ('attr_label', models.CharField(default=b'default', max_length=200, null=True)),
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
                ('name', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('amount', models.IntegerField(default=0, null=True, blank=True)),
                ('size', models.CharField(default=b'', max_length=40, null=True, blank=True)),
                ('classify', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('type', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('material', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('technique', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('description', models.TextField(default=b'', max_length=1000, null=True, blank=True)),
                ('identifier', models.CharField(default=b'', max_length=50, null=True, blank=True)),
                ('image', models.ImageField(default=b'default.jpg', null=True, upload_to=b'images/')),
                ('author', models.CharField(default=b'', max_length=100, null=True, blank=True)),
                ('price', models.CharField(default=b'', max_length=50, null=True, blank=True)),
                ('date_creation', models.CharField(default=b'', max_length=50, null=True, blank=True)),
                ('place_of_creation', models.CharField(default=b'', max_length=50, null=True, blank=True)),
                ('date_detection', models.CharField(default=b'', max_length=50, null=True, blank=True)),
                ('place_detection', models.CharField(default=b'', max_length=50, null=True, blank=True)),
                ('date_existence', models.CharField(default=b'', max_length=50, null=True, blank=True)),
                ('place_existence', models.CharField(default=b'', max_length=50, null=True, blank=True)),
                ('mark_on_object', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('note', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('condition', models.CharField(default=b'', max_length=100, null=True, blank=True)),
                ('condition_descr', models.CharField(max_length=2000, null=True, blank=True)),
                ('transport_possibility', models.BooleanField(default=False)),
                ('recomm_for_restauration', models.CharField(default=b'', max_length=100, null=True, blank=True)),
                ('restauration_notes', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('memorial_subject', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('storage', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('place_appellation', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('is_there', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('bibliography', models.CharField(default=b'', max_length=1000, null=True, blank=True)),
                ('way_of_found', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('link_on_doc', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('side_1', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('side_2', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('term_back', models.DateField(default=b'2000-01-01', null=True, blank=True)),
                ('aim_of_receiving_gen', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('circumst_write_off', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('reason', models.FileField(default=b'default.txt', null=True, upload_to=b'docs/')),
                ('stat', models.CharField(default=b'\xd0\x9f\xd1\x83\xd1\x81\xd1\x82\xd0\xb8\xd0\xb9 \xd0\xbe\xd0\xb1\xe2\x80\x99\xd1\x94\xd0\xba\xd1\x82', max_length=200, blank=True)),
            ],
            options={
                'permissions': (('see_all_obj', '\u0431\u0430\u0447\u0438\u0442\u0438 \u0432\u0441i'), ('see_personal_obj', '\u0431\u0430\u0447\u0438\u0442\u0438 \u0441\u0432\u043ei'), ('action_obj', '\u043e\u0431\u043bi\u043a\u043e\u0432i \u043f\u0440\u043e\u0446\u0435\u0434\u0443\u0440\u0438'), ('add_new_obj', '\u0434\u043e\u0434\u0430\u0432\u0430\u043d\u043d\u044f'), ('change_obj', '\u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u043d\u043d\u044f'), ('remove_obj', '\u0432\u0438\u0434\u0430\u043b\u0435\u043d\u043d\u044f')),
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
        migrations.AddField(
            model_name='activity',
            name='aim',
            field=models.ForeignKey(to='mainapp.Object', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='myUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='activity',
            name='actor',
            field=models.ForeignKey(to='mainapp.myUser'),
            preserve_default=True,
        ),
    ]
