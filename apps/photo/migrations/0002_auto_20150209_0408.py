# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packtranslation',
            name='description',
            field=models.TextField(verbose_name='description', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='packtranslation',
            name='title',
            field=models.CharField(verbose_name='title', max_length=200),
            preserve_default=True,
        ),
    ]
