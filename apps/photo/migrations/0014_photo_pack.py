# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0013_auto_20141215_0635'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='pack',
            field=models.ManyToManyField(to='photo.Pack'),
            preserve_default=True,
        ),
    ]
