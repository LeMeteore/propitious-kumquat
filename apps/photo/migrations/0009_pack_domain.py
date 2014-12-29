# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0008_auto_20141215_0557'),
    ]

    operations = [
        migrations.AddField(
            model_name='pack',
            name='domain',
            field=models.CharField(default='politique', max_length=200),
            preserve_default=False,
        ),
    ]
