# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0003_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='pack',
            name='country',
            field=models.ManyToManyField(to='photo.Country'),
            preserve_default=True,
        ),
    ]
