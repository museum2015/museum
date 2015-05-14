# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('mainapp', '0003_auto_20150513_1531'),
    ]

    operations = [
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
            model_name='object',
            name='reason',
            field=models.FileField(default=b'default.txt', null=True, upload_to=b'/docs'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='actor',
            field=models.ForeignKey(to='mainapp.myUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='object',
            name='image',
            field=models.ImageField(default=b'default.jpg', null=True, upload_to=b'/images'),
            preserve_default=True,
        ),
    ]
