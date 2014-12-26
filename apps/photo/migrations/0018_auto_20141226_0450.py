# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0017_auto_20141226_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='packtranslation',
            name='description',
            field=models.CharField(max_length=200, default='une description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='packtranslation',
            name='label',
            field=models.CharField(max_length=200, default='un label'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phototranslation',
            name='description',
            field=models.CharField(max_length=200, default='une description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phototranslation',
            name='label',
            field=models.CharField(max_length=200, default='un label'),
            preserve_default=False,
        ),
    ]
