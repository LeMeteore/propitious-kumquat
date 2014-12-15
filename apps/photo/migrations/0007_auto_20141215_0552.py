# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0006_auto_20141215_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pack',
            name='description',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
